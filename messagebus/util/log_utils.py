import logging

LOG_FORMAT = '%(levelname)-5s %(asctime)s %(filename)s:%(lineno)d: %(message)s'

def init(level=logging.DEBUG):
    logging.basicConfig(level=level, format=LOG_FORMAT)
