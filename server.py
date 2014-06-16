import tornado.ioloop
import sys
import tornado.web
import application as app

if __name__ == "__main__":
    PORT = sys.argv[1] if len(sys.argv) > 1 else 8888
    app.application.listen(PORT)
    print 'Development server is running at http://127.0.0.1:%s' % PORT
    print 'Quit the server with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()
