import json


class Response:
    content_type = "text/plain"
    _headers = None
    _body = None

    def __init__(self, body="", status=200, headers=dict(), content_type=None):

        if content_type is not None:
            self.content_type = content_type

        self._headers = headers
        self.status = status
        self.body = body

    @property
    def headers(self):
        if not "Content-Type" in self._headers:
            self._headers["Content-Type"] = self.content_type

        if not "Content-Length" in self._headers:
            self._headers["Content-Length"] = len(self.body)

        return self._headers

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self.set_body(value)

    def set_body(self, value):
        if isinstance(value, str):
            self._body = value.encode()
        elif isinstance(value, bytes):
            self._body = value

class JsonResponse(Response):
    content_type = "application/json"
    def set_body(self, value):
        self._body = json.dumps(value).encode()
