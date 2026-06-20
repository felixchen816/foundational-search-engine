"""Small standard-library web interface for local search."""

from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Optional, Sequence, Tuple
from urllib.parse import parse_qs, urlparse

from search_engine.search import SearchResult, search_documents
from search_engine.loader import load_documents
from search_engine.semantic import expand_query_text


DEFAULT_DATA_DIRECTORY = "data/example_corpus"


def render_search_page(
    query: str = "",
    results: Optional[Sequence[SearchResult]] = None,
    error: str = "",
    data_directory: str = DEFAULT_DATA_DIRECTORY,
    mode: str = "keyword",
) -> str:
    """Render the search form and optional results."""
    safe_query = escape(query)
    safe_data = escape(data_directory)
    keyword_checked = "checked" if mode == "keyword" else ""
    semantic_checked = "checked" if mode == "semantic" else ""
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Foundational Search Engine</title>",
        "<style>",
        "body{font-family:system-ui,-apple-system,sans-serif;margin:2rem;line-height:1.5;max-width:860px}",
        "form{display:grid;gap:.75rem;margin:1.5rem 0}",
        "input,button{font:inherit;padding:.6rem .7rem}",
        "button{cursor:pointer}",
        ".result{border-top:1px solid #ddd;padding:1rem 0}",
        ".score{color:#555;font-size:.9rem}",
        ".error{color:#9b1c1c}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Foundational Search Engine</h1>",
        '<form action="/search" method="get">',
        '<input name="q" value="{}" placeholder="Search local documents" autofocus>'.format(safe_query),
        '<input name="data" value="{}" aria-label="Data directory">'.format(safe_data),
        '<label><input type="radio" name="mode" value="keyword" {}> Keyword</label>'.format(keyword_checked),
        '<label><input type="radio" name="mode" value="semantic" {}> Semantic</label>'.format(semantic_checked),
        "<button type=\"submit\">Search</button>",
        "</form>",
    ]

    if error:
        body.append('<p class="error">{}</p>'.format(escape(error)))

    if results is not None:
        if results:
            body.append("<ol>")
            for result in results:
                body.append(
                    '<li class="result"><strong>{}</strong> <span class="score">score={:.3f}</span><br>{}</li>'.format(
                        escape(result.doc_id),
                        result.score,
                        escape(result.preview),
                    )
                )
            body.append("</ol>")
        elif query:
            body.append("<p>No results</p>")

    body.extend(["</body>", "</html>"])
    return "\n".join(body)


def search_request(query: str, data_directory: str = DEFAULT_DATA_DIRECTORY, mode: str = "keyword") -> Tuple[str, int]:
    """Return rendered HTML and status for one search request."""
    normalized_mode = mode if mode in {"keyword", "semantic"} else "keyword"
    if not query.strip():
        return render_search_page(query=query, data_directory=data_directory, mode=normalized_mode), 200

    try:
        documents = load_documents(data_directory)
        search_query = expand_query_text(query) if normalized_mode == "semantic" else query
        results = search_documents(documents, search_query)
    except (FileNotFoundError, NotADirectoryError) as exc:
        return render_search_page(query=query, error=str(exc), data_directory=data_directory, mode=normalized_mode), 400

    return render_search_page(query=query, results=results, data_directory=data_directory, mode=normalized_mode), 200


class SearchRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the local search UI."""

    data_directory = DEFAULT_DATA_DIRECTORY

    def do_GET(self) -> None:
        """Serve the search form or query results."""
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_html(render_search_page(data_directory=self.data_directory), 200)
            return
        if parsed.path == "/search":
            query_params = parse_qs(parsed.query)
            query = query_params.get("q", [""])[0]
            data_directory = query_params.get("data", [self.data_directory])[0]
            mode = query_params.get("mode", ["keyword"])[0]
            html, status = search_request(query, data_directory=data_directory, mode=mode)
            self._send_html(html, status)
            return

        self._send_html(render_search_page(error="Not found", data_directory=self.data_directory), 404)

    def log_message(self, format: str, *args) -> None:
        """Silence default request logs in CLI usage."""

    def _send_html(self, html: str, status: int) -> None:
        content = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run_server(host: str = "127.0.0.1", port: int = 8000, data_directory: str = DEFAULT_DATA_DIRECTORY) -> None:
    """Run the local search web server."""
    handler = type("ConfiguredSearchRequestHandler", (SearchRequestHandler,), {"data_directory": data_directory})
    server = HTTPServer((host, port), handler)
    print("Serving search UI at http://{}:{} using {}".format(host, port, data_directory))
    server.serve_forever()
