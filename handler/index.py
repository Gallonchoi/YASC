import logging
import tornado.web
import tornado.websocket
import tornado.escape
import tornado.auth

from time import time


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")


class MessageHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    clients = set()
    message_buffer = []

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
        except:
            logging.error("It seems something wrong")

    @classmethod
    def update_buffer(cls, chat):
        cls.message_buffer.append(chat)

    def open(self):
        MessageHandler.clients.add(self)
        logging.info("Sending message to the new client")
        for message in self.message_buffer:
            self.write_message(message)
        logging.info("WebSocket opened!")
        logging.info("There are %s polls" % len(MessageHandler.clients))

    def on_message(self, message):
        if message == False:
            return
        chat = {
            "type": "message",
            "username": self.get_current_user(),
            "message": message,
            "time": time()*1000
            }
        MessageHandler.update_buffer(chat)
        MessageHandler.send_to_all(chat)

    def on_close(self):
        MessageHandler.clients.remove(self)
        logging.info("WebSocket closed!")


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
