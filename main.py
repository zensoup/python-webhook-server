from webhookserver.response import JsonResponse, Response
from webhookserver.server import BaseWebHookServer, Handler

handler = Handler(callback=lambda x, y: JsonResponse({"hoho": "lala"}))
server = BaseWebHookServer()
server.register("", handler)
