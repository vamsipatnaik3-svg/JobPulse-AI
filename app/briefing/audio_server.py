
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

AUDIO_FILE = (
    Path(__file__).resolve().parents[2]
    / "generated_audio"
    / "jobpulse_briefing.mp3"
)

class AudioHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != "/latest-audio":
            self.send_error(404, "Not found")
            return

        if not AUDIO_FILE.exists():
            self.send_error(404, "Briefing audio not generated yet")
            return

        audio = AUDIO_FILE.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Content-Length", str(len(audio)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(audio)

    def log_message(self, format, *args):
        print(format % args)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AudioHandler)
    print("JobPulse audio server running on port 8000")
    print("Keep this terminal open while testing.")
    server.serve_forever()
