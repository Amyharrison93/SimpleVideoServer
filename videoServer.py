import http.server
import socketserver
import os
import json

with open('VideoConfig.json', 'r') as file:
    data = file.read()
parsed_data = json.loads(data)

PORT = 8000
DIRECTORY = parsed_data['VideoDirectory']
print(DIRECTORY)

if not os.path.exists(DIRECTORY):
    exit()

class VideoRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        # Send response headers
        path = self.path.strip("/")  # Remove leading slash
        full_path = os.path.join(DIRECTORY, path)

        if os.path.isfile(full_path):
            # Get the appropriate mime type
            mime_type = 'video/mp4'
            self.send_response(200)
            self.send_header("Content-type", mime_type)
            self.end_headers()
            return open(full_path, 'rb')
        else:
            self.send_error(404, "File not found")
            return None

    def do_GET(self):
        # Serve videos from the specified directory
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

# Set up the HTTP server
handler = VideoRequestHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving videos at http://localhost:{PORT}")
    httpd.serve_forever()
