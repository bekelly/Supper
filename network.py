# network.py

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from artwork import get_artwork

HOST = "0.0.0.0"
PORT = 8000

def start_listener(renderer, host=HOST, port=PORT):
    """
    Launch an HTTP server that listens for /nowplaying requests
    and uses the provided renderer to display the artwork.
    """

    class NowPlayingHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path != "/nowplaying":
                self.send_response(404)
                self.end_headers()
                return

            qs = parse_qs(parsed.query)
            artist = qs.get("artist", [""])[0]
            album  = qs.get("album",  [""])[0]
            track  = qs.get("track",  [""])[0]
            state  = qs.get("state",  [""])[0].lower()

            # Validate inputs
            if not artist or not album or not track or state not in ("playing", "paused"):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(
                    b"Usage: /nowplaying?artist=...&album=...&track=...&state=playing|paused"
                )
                return

            try:
                # 1) Get artwork (downloads if needed)
                art_path = get_artwork(artist, album)

                # 2) Render it immediately
                renderer.show_image(str(art_path))

                # 3) Respond with JSON
                resp = {
                    "status": "ok",
                    "artist": artist,
                    "album": album,
                    "track": track,
                    "state": state,
                    "path": str(art_path),
                }
                body = json.dumps(resp).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            except Exception as e:
                err = {"status": "error", "message": str(e)}
                body = json.dumps(err).encode("utf-8")

                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        def log_message(self, fmt, *args):
            # Silence default logging
            return

    server = ThreadingHTTPServer((host, port), NowPlayingHandler)
    print(f"[network] NowPlaying listener running on http://{host}:{port}")
    server.serve_forever()