# VLWS - Very Light Web Server

VLWS is an experimental light web server using sockets - low-level networking interface.
You need python3 (3.6) to run this web server.

Please run the web server:
```
# python server/server.py -p <port number>
```

### Go on your browser to: http://localhost:<port number>, and you should see an index-page.

If you want, you can add extra content to the www-data -folder.
Web server is capable to deliver web pages (.htm / .html / .txt) to the client.

There are unit-tests included for the web server.
You can run the tests with the following command:
```
# python -m unittest server/tests/test_server.py
```
