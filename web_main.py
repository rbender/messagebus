import logging

from webapp import server

logging.basicConfig(level=logging.DEBUG)

server.app.run()