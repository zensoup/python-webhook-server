from webhookserver.server import BaseWebHookServer, Handler


handler = Handler(callback=lambda x, y: b'{"hoho": "lala"}')
server = BaseWebHookServer()
server.register("", handler)
