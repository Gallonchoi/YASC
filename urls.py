from handler import index

urls = [
    (r'/', index.MainHandler),
    (r'/login', index.AuthLoginHandler),
    (r'/logout', index.AuthLogoutHandler),
    (r'/message', index.MessageHandler),
    ]
