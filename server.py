import http.server
import socketserver
import json
from urllib.parse import urlparse


class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        print(query)
        question = query
        response = handle_query(query)
        send = "{'Response', ['question':('" + question + "'), 'response':('" + response + "')]}"
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(send, 'utf8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

    def to_upper_case(question):
        return question.upper()


def handle_query(query):
    if query == 'test':
        return 'so this is a test?'
    else:
        return 'oh well'
if __name__ == "__main__":
    print('Server listening on port 8000...')
    httpd = socketserver.TCPServer(('', 8000), Server)
    httpd.serve_forever()
