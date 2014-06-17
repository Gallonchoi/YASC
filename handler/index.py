import logging
import tornado.web
import tornado.websocket
import tornado.escape
import tornado.auth


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html", messages=MessageHandler.message_buffer)


class MessageHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    clients = set()
    message_buffer = []

    @staticmethod
    def send_to_all(message):
        for client in MessageHandler.clients:
            client.write_message(message)

    def open(self):
        MessageHandler.clients.add(self)
        logging.info("WebSocket opened!")
        logging.info("There are %s polls" % len(MessageHandler.clients))

    def on_message(self, message):
        text = {
            "type": "message",
            "username": self.get_current_user(),
            "message": message
            }
        MessageHandler.message_buffer.append(text)
        self.send_to_all(text)

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
