import logging
import sys
import tornado.ioloop
import tornado.web
import application

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)


if __name__ == "__main__":
    parse_command_line()
    logging.info('Development server is running at http://127.0.0.1:%s' % options.port)
    logging.info('Quit the server with CONTROL-C')
    app = application.Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
