import tornado.web
import os

from urls import urls

SETTINGS = dict(
    cookie_secret="abcdefghijklmnopqrstuvwxyz123456",
    login_url="/login",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=True,
    debug=True,
    )
application = tornado.web.Application(
    handlers=urls,
    **SETTINGS
    )
