#!/usr/bin/env python3
"""Does each book's 404 page find its own assets? Serves the shared `docs` root as the book says to, with one difference a real static host has: an unknown path under a book answers that book's 404.html.
For each book, request an unknown path, parse what the served page asks for, and fetch each. A row is broken if the browser would resolve it to a path that answers 404.
usage: python3 -B scripts/serve_book_404.py docs  (after `make book`); exit 1 when any asset would 404 (D80, LIVE-CONTAINMENT.4)"""
import functools, html.parser, http.server, sys, threading, urllib.error, urllib.parse, urllib.request
from pathlib import Path
DOCS = Path(sys.argv[1]).resolve()
BOOKS = sorted(p.relative_to(DOCS).parent.as_posix() for p in DOCS.glob("**/book/404.html") if "/api/" not in str(p))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def send_error(self, code, message=None, explain=None):
        path = urllib.parse.urlparse(self.path).path.lstrip("/")
        for b in BOOKS:
            if code == 404 and path.startswith(b + "/"):
                body = (DOCS / b / "404.html").read_bytes()
                self.send_response(404); self.send_header("Content-Type", "text/html"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
                return
        super().send_error(code, message, explain)
class P(html.parser.HTMLParser):
    def __init__(self): super().__init__(); self.base = None; self.refs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "base" and self.base is None: self.base = a.get("href")
        if tag == "link" and a.get("rel") == "stylesheet" and a.get("href"): self.refs.append(a["href"])
        if tag == "script" and a.get("src"): self.refs.append(a["src"])
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(H, directory=str(DOCS)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
root = f"http://127.0.0.1:{srv.server_address[1]}/"
total_bad = 0
for b in BOOKS:
    url = root + b + "/no/such/page.html"
    try:
        body = urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as e:
        body = e.read()
    p = P(); p.feed(body.decode("utf-8", "replace"))
    base = urllib.parse.urljoin(url, p.base or "")
    bad = []
    for r in p.refs:
        target = urllib.parse.urljoin(base, r)
        if not target.startswith(root): continue
        try:
            urllib.request.urlopen(target).read()
        except urllib.error.HTTPError as e:
            bad.append((e.code, target[len(root):]))
    total_bad += len(bad)
    print(f"{b}: base {p.base!r}, {len(p.refs)} assets, {len(bad)} broken{(' e.g. ' + bad[0][1]) if bad else ''}")
print(f"books {len(BOOKS)}, broken assets {total_bad}")
srv.shutdown(); sys.exit(1 if total_bad else 0)
