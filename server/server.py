#!/usr/bin/python3

import create_server
import sys


def usage():
    print("Usage: python server.py -p|--port <port number>")


def main(argv):

    if len(argv) != 2:
        usage()
        sys.exit()

    if not(argv[0] == "-p" or argv[0] == "--port"):
        usage()
        sys.exit()

    try:
        port = int(argv[1])
    except ValueError:
        print("Port is not an integer.")
        sys.exit()

    create_server.bind_to_port(port)
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
