import webapp2
import hmac
import hashlib
import os
import jinja2

from baseHandler.views import *

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.request.headers["content-Type"] = 'text/plain;charset=utf-8'
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def login(self, name, val):
        cookie_hash = make_cookie_hash(val)
        self.response.headers.add_header("Set-Cookie", "%s=%s; Path=/" % (name, cookie_hash))

    def logout(self, name):
        self.response.headers.add_header("Set-Cookie", "%s=; Path=/" % (name))

    def get_cookie_hash(self, name):
        return self.request.cookies.get(str(name))

    def get_user_id(self, hash):
        return hash.split("|")[0]

    def getLoggedInUser(self):

        cookie_hash = self.get_cookie_hash("user")
        userId = None

        if check_cookie_hash(cookie_hash):
            userId = int(self.get_user_id(cookie_hash))

        if not userId:
            return None
        else:
            return userId
