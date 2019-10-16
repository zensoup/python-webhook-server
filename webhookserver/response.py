import json
from wsgiref.headers import Headers


class Response:
    status = "200 OK"
    content_type = "text/plain"

    def __init__(self, body, status=None, headers=Headers(), content_type=None):
        if status:
            self.status = status
        if content_type is not None:
            self.content_type = content_type
        self.headers = headers
        self.body = body
        if "Content-Type" not in headers:
            self.headers["Content-Type"] = self.content_type

        if "Content-Length" not in headers:
            self.headers["Content-Length"] = str(len(self._body))

    @property
    def body(self):
        return self._body.decode()

    @body.setter
    def body(self, value):
        self.set_body(value)

    def set_body(self, value):
        if isinstance(value, str):
            self._body = value.encode()
        elif isinstance(value, bytes):
            self._body = value
        self.headers["content-length"] = str(len(self._body))

    def get_response_body(self):
        return [self._body]


class JsonResponse(Response):
    content_type = "application/json"

    def set_body(self, value):
        body = json.dumps(value)
        self._body = body.encode()
        self.headers["content-length"] = str(len(self._body))
