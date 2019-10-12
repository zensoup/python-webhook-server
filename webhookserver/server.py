from functools import singledispatch
import json
from urllib.parse import parse_qs
from typing import Callable


class Handler:
    def __init__(self, callback=None):
        if callable(callback):
            self.handle = callback

    def handle(self, path, method, query):
        raise NotImplementedError(
            "You have not specified a handle method for this Handler."
        )


class BaseWebHookServer:
    _hooks = {}

    def register(self, path: str, handler: Callable):
        """
        Register a new callback to be executed when /<path>/ is accessed.
        """
        self._hooks.update({path.rstrip("/"): handler})

    def serve_request(self, env: dict, start_response: Callable):
        """
        The wsgi application callable.
        """
        path, method, query = parse_wsgi_env(env)

        handler, remaining_path = self._get_handler(path)
        data = handler.handle(remaining_path, method, query)

        status = "200 OK"
        response_headers = [
            ("Content-type", "application/json"),
            ("Content-Length", str(len(data))),
        ]
        start_response(status, response_headers)
        return [data]

    def _get_handler(self, path: str) -> Handler:
        """
        Read the requested path and find the appropriate handler.
        """
        for registered_path, handler in self._hooks.items():
            if path.startswith(registered_path + "/"):
                relpath = path.replace(registered_path, "")
                return handler, relpath

    def __call__(self, *args, **kwargs):
        return self.serve_request(*args, **kwargs)


def parse_wsgi_env(environ: dict):
    """
    Parse a wsgi environment dictionary and return the request path, the
    query string and the request method as a three-tuple.
    """
    query = parse_qs(environ["QUERY_STRING"])
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    return path, method, query
