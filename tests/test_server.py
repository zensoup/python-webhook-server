import re
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock
from webhookserver.server import BaseWebHookServer


class TestBaseServer(TestCase):
    def test_match_path(self):
        handler = Mock()
        hooks = {re.compile(r"/people"): handler}
        obj = SimpleNamespace(_hooks=hooks)
        match = BaseWebHookServer._match_handler(obj, "/people")
        self.assertEqual(match, handler)
