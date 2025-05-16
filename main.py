from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/contacts.html":
            self.respond_with_file("contacts.html")
        else:
            self.send_error(404, "Файл не найден")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = parse_qs(post_data)

        print("Получены POST-данные:")
        for key, values in parsed_data.items():
            for value in values:
                print(f"{key}: {value}")

        self.respond_with_file("contacts.html")

    def respond_with_file(self, filename):
        try:
            with open(filename, "rb") as f:
                content = f.read()
            self.send_response(200)
            content_type = self.guess_content_type(filename)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f"Файл {filename} не найден")


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Сервер запущен на http://localhost:8000")
    httpd.serve_forever()
