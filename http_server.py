import os
import socket
import sys


def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->

        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    # TODO: Implement response_ok -> OK

    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body,
    ])


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # TODO: Implement response_method_not_allowed -> OK
    return b"\r\n".join([
        b"HTTP/1.1 405 Method Not Allowed",
        b"",
        b"You can't do that on this server!"
    ])


def response_not_found():
    """Returns a 404 Not Found response"""

    # TODO: Implement response_not_found -> OK
    return b"\r\n".join([
        b"HTTP/1.1 404 Not Found response",
        b"",
        b"You can't find this URL!"
    ])

def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    # TODO: implement parse_request
    
    method, path, version = request.split("\r\n")[0].split(" ")

    if method != "GET":
        raise NotImplementedError

    return path


def response_path(path):
    """
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """
    try:
        with open('webroot' + path, 'rb') as f:
            content = f.read()
    except FileNotFoundError:
        raise NameError
    except IsADirectoryError:
        content = "\r\n".join(os.listdir('webroot' + path))
        content = content.encode()

    if ".png" in path:
        mime_type = b"image/png"
    elif ".jpg" in path:
        mime_type = b"image/jpeg"
    elif ".html" in path:
        mime_type = b"text/html"
    elif ".py" in path:
        # Rub the .py script and use the resulting html as the response body
        file_name = 'webroot' + path[-(path[::-1].find('/') + 1):]
        res = subprocess.run(["python", file_name], stdout=subprocess.PIPE)
        content = res.stdout
        mime_type = b"text/html"

    else:
        mime_type = b"text/plain"

    return content, mime_type



def server(log_buffer=sys.stderr):
    address = ('0.0.0.0', int(os.environ.get('PORT', 10000)))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break

                #print("Request received:\n{}\n\n".format(request))

                try:

                    # TODO: Use parse_request to retrieve the path from the request. -> OK

                    path = parse_request(request)

                    # TODO: Use response_path to retrieve the content and the mimetype,
                    # based on the request path. -> OK

                except NotImplementedError:
                    response = response_method_not_allowed()


                else:

                    try:
                        content, mimetype = response_path(path)
                        response = response_ok(body=content, mimetype=mimetype)                        

                    except NameError:
                        response = response_not_found()

                conn.sendall(response)

            finally:
                conn.close() 

    except KeyboardInterrupt:
        sock.close()

if __name__ == '__main__':
    server()
    sys.exit(0)

