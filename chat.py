from time import time
import logging
import uuid
import os

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")


class MessageHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    all_users = []
    message_buffer = []

    def get_current_user(self):
        cur_user = self.get_secure_cookie("user")
        if cur_user:
            return cur_user.decode('utf-8')

    @classmethod
    def send_to_all(cls, chat):
        logging.info("Sending message to %d waiters", len(cls.clients))
        try:
            for client in cls.clients:
                if type(chat) == list:
                    for message in chat:
                        client.write_message(message)
                else:
                    client.write_message(chat)
        except Exception as e:
            logging.error("It seems something wrong! " + str(e))

    @classmethod
    def update_buffer(cls, chat):
        cls.message_buffer.append(chat)

    def open(self):
        cur_user = self.get_current_user()
        if not cur_user:
            logging.warning("Unauthorized entry: open new websocket")
            self.close(None, "Unauthorized entry")
            return
        MessageHandler.clients.add(self)
        MessageHandler.all_users.append(cur_user)
        logging.info("Sending message to the new client")
        MessageHandler.update_user_list()
        for message in self.message_buffer:
            self.write_message(message)
        logging.info("WebSocket opened! New user: " + cur_user)
        logging.info("There are %s polls" % len(MessageHandler.clients))

    def on_message(self, message):
        cur_user = self.get_current_user()
        if not message or not cur_user:
            logging.warning("Unauthorized entry: sending message")
            self.close(None, "Unauthorized entry")
            return
        chat = {
            "type": "message",
            "username": cur_user,
            "message": message,
            "time": time()*1000
            }
        MessageHandler.update_buffer(chat)
        MessageHandler.send_to_all(chat)

    @classmethod
    def update_user_list(cls):
        user_list = {
            "type": "userlist",
            "users": cls.all_users
            }
        MessageHandler.send_to_all(user_list)

    def on_close(self):
        cur_user = self.get_current_user()
        MessageHandler.clients.remove(self)
        MessageHandler.all_users.remove(cur_user)
        logging.info("One websocket closed!")
        MessageHandler.update_user_list()


class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/login', AuthLoginHandler),
            (r'/logout', AuthLogoutHandler),
            (r'/message', MessageHandler),
        ]
        settings = dict(
            cookie_secret=uuid.uuid4().hex,
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    parse_command_line()
    logging.info("Development server is running at http://127.0.0.1:%s"
                 % options.port)
    logging.info("Quit the server with CONTROL-C")
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
