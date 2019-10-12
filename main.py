from webhookserver.server import BaseWebHookServer, Handler


handler = Handler(callback=lambda x, y, z: b'{"hoho": "lala"}')
server = BaseWebHookServer()
server.register("", handler)
