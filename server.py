import tornado.ioloop
import sys
import tornado.web
import application as app

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)


if __name__ == "__main__":
    parse_command_line()
    print 'Development server is running at http://127.0.0.1:%s' % options.port
    print 'Quit the server with CONTROL-C'
    app.application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
