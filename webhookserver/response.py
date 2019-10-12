class Response:
    def __init__(self, body, status=200, headers=dict(), content_type="text/plain"):

        if not "Content-Type" in headers:
            headers["Content-Type"] = content_type

        if not "Content-Length" in headers:
            headers["Content-Length"] = len(self.body)

        self.status = status

    @property
    def body(self):
        return self._body

    @body.setter
    def set_body(self, value):
        if isinstance(body, str):
            self.body = body.encode()
        elif isinstance(body, bytes):
            self.body = body
