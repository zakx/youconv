from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from youconv import app

http_server = HTTPServer(WSGIContainer(app))
http_server.bind(8888, address="127.0.0.1")
http_server.start(0)
IOLoop.instance().start()
