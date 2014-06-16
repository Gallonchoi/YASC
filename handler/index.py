import tornado.web
import tornado.websocket
import tornado.escape
import tornado.auth

from model.message import message_buffer

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        messages = message_buffer.get()
        self.render("index.html", messages=messages)

class MessageHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    clients = set()

    @staticmethod
    def send_to_all(message):
        for client in MessageHandler.clients:
            client.write_message(message)

    def open(self):
        print "WebSocket opened!"
        info = {
            "username": "Server",
            "message": "Welcome to Simple Chat!"
            }
        self.write_message(info)
        MessageHandler.clients.add(self)
        info = {
            "username": "Server",
            "message": "There is a new player: " + self.get_current_user()
            }
        self.send_to_all(info)

    def on_message(self, message):
        text = {
            "username": self.get_current_user(),
            "message": message
            }
        self.send_to_all(text)

    def on_close(self):
        try:
            MessageHandler.clients.remove(self)
            print "WebSocket closed!"
        except:
            print MessageHandler.clients

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
