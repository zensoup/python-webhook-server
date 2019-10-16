import re
from typing import Callable

from webhookserver.response import Response

# from urllib.parse import parse_qs



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
    _hooks = dict()

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
        path = env["PATH_INFO"]

        match = self._match_handler(path)
        if not match:
            return None

        handler = match.handler

        response = handler.handle(env, match)
        if not isinstance(response, Response):
            raise ValueError("Handlers must return an instance of Response.")

        start_response(response.status, response.headers.items())
        return response.get_response_body()

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
