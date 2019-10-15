import re
from functools import singledispatch
import json
from urllib.parse import parse_qs
from typing import Callable


class Handler:
    def __init__(self, callback=None):
        if callable(callback):
            self.handle = callback

    def handle(self, request: dict, match: "UrlMatch"):
        raise NotImplementedError(
            "You have not specified a handle method for this Handler."
        )


class UrlMatch:
    """
    A simple container class for routes matched by a requested URL.
    """

    def __init__(self, handler, path, match):
        self.handler = handler
        self.groups = match.groups()
        self.named_groups = match.groupdict()
        self.path = path[match.end() :]
        self.full_path = path
        self._matchobj = match


class BaseWebHookServer:
    _hooks = {}

    def register(self, path: str, handler: Callable):
        """
        Register a new callback to be executed when /<path>/ is accessed.
        """
        path_regex = re.compile(path)
        self._hooks.update({path_regex: handler})

    def serve_request(self, env: dict, start_response: Callable):
        """
        The wsgi application callable.
        """
        path, method, query = parse_wsgi_env(env)

        match = self._match_handler(path)
        if not match:
            return None

        handler = match.handler

        data = handler.handle(env, match)

        status = "200 OK"
        response_headers = [
            ("Content-type", "application/json"),
            ("Content-Length", str(len(data))),
        ]
        start_response(status, response_headers)
        return [data]

    def _match_handler(self, path: str) -> (Handler, list, dict):
        """
        Read the requested path and find the appropriate handler.

        Returns the matched handler, a list of unnamed groups and a dict of
        named groups that may exist in the regular expression.
        """
        for path_regex, handler in self._hooks.items():
            match = path_regex.search(path)
            if match:
                return UrlMatch(handler, path, match)
        return None

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
