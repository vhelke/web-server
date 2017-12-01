import re
import select
import socket
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def check_file_type(url):
    # We support directories (such as "/" or "/foo/"), and file-types: *.htm *.html and *.txt
    if len(url) < 1:
        return False
    elif url[0] != "/":
        return False  # First character must be "/"
    elif "//" in url or ".." in url:  # A simple security check, disallow e.g. /../
        return False
    elif url[0] == "/" and url[-1] == "/" and "." in url:
        return False  # /file.txt/ not allowed
    elif re.search("[A-Za-z0-9_-]\.[a-z]+$", url):  # if url ends with a dot something, make sure "something" is letters
        if url[-4:] == ".htm" or url[-5:] == ".html" or url[-4:] == ".txt":  # explicit check
            return True
        else:
            return False
        return False
    elif "." not in url:  # e.g. /foo/bar or /foo_bar
        return True
    else:
        return False


def get_error_page():
    try:
        f = open("templates/error.html")
        return {"header": "HTTP/1.0 404 Not found\r\n\r\n", "file": f}
    except FileNotFoundError:
        sys.exit(5)  # unexpected error


def get_file(url):
    # If URL=directory, we check if there is "index.htm" or "index.html" and we show that one,
    # otherwise we return HTTP 404 - Not found.
    file_type_or_directory_ok = check_file_type(url)

    if not file_type_or_directory_ok:
        return get_error_page()

    elif file_type_or_directory_ok and "." not in url:  # directory
        slash = ""
        if url[-1] != "/":
            slash = "/"  # append url: /foo --> /foo/

        try:
            f = open("www-data" + url + slash + "index.html")
        except FileNotFoundError:
            try:
                f = open("www-data" + url + slash + "index.htm")
            except FileNotFoundError:
                return get_error_page()
    else:  # file
        try:
            f = open("www-data" + url)
        except FileNotFoundError:
            return get_error_page()

    return {"header": "HTTP/1.0 200 OK\r\n\r\n", "file": f}


def get_request(data):
    # 'data' is a multiline header, take the first line to get the requested URL
    first_line = data.split('\n', 1)[0]
    first_line_array = first_line.split()  # Should be similar to ['GET', '/', 'HTTP/1.1']
    if len(first_line_array) != 3:
        eprint("Request is not understood.")
        return {"successful": False, "url": None}

    if first_line_array[0] != "GET":
        eprint("Only GET-requests are supported.")
        return {"successful": False, "url": None}

    # URLs should start with "/"
    requested_url = first_line_array[1]
    if requested_url[0] != "/":
        eprint("Requested URL not found.")
        return {"successful": False, "url": None}

    return {"successful": True, "url": requested_url}


def bind_to_port(port):

    BUFF_SIZE = 1024
    LISTEN_QUEUE = 5  # queue up as many as 5 connect requests (the normal max according to docs.python.org)
    SERVER_NAME = "localhost"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # so that socket can be immediately reused after Ctrl-C

    try:
        server.bind((SERVER_NAME, port))
    except OSError:
        eprint("Address already in use.")
        return

    server.listen(LISTEN_QUEUE)
    readers = [server]

    print("Shutdown the web server with Ctrl-C.")

    while True:
        ready_to_read = None
        try:
            ready_to_read, ready_to_write, in_error = select.select(readers, [], [])
            for s in ready_to_read:
                if s == server:
                    client, address = server.accept()
                    readers.append(client)  # select on this socket next time
                else:
                    # Not the server's socket, so we'll read
                    data = s.recv(BUFF_SIZE)
                    if data:
                        request = get_request(data.decode('utf-8'))
                        if request["successful"]:
                            fetch = get_file(request["url"])
                            try:
                                s.send(fetch["header"].encode("utf-8"))  # send the HTTP-header
                            except (ConnectionResetError, BrokenPipeError):
                                    pass
                            file = fetch["file"]

                            try:
                                outputdata = file.read()
                            except UnicodeDecodeError:
                                eprint("Exiting because of non-supported content.")
                                sys.exit(6)
                            file.close()
                            for i in range(0, len(outputdata)):
                                try:
                                    s.send(outputdata[i].encode("utf-8"))  # send the actual requested HTTP-page
                                except (ConnectionResetError, BrokenPipeError):
                                    pass
                    s.close()
                    readers.remove(s)
        except KeyboardInterrupt:
            if ready_to_read:
                for s in ready_to_read:
                    if s == server:
                        pass
                    else:
                        s.close()
            break  # jump out of 'while True' -> close server

    # clean up
    server.close()
