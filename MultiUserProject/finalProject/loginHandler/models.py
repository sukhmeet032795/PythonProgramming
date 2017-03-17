from baseHandler.models import BaseHandler
from userHandler.models import User
from loginHandler.views import *
from signupHandler.views import *
import re
import hashlib
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Login(BaseHandler):

    def get(self):
        userId = self.getLoggedInUser()

        if userId:
            self.redirect("/wall")
        else:
            self.render("login.html", user = 0)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        p = {"username" : username}
        error = False

        if not valid_username(username):
            p["error_username"] = "Username is not valid"
            error = True

        if not valid_password(password):
            p["error_password"] = "Password is not valid(Can't be Empty)"
            error = True

        if error:
            return self.render("login.html", **p)

        user = User.by_username(username)

        if not user:
            p["error_form"] = "No such user exists"
            p["user"] = 0
            return self.render("login.html", **p)
        else:
            p["user"] = user
            if not check_pw_hash(username, password, user.pw_hash):
                p["error_form"] = "UserName/Password combination is invalid"
                return self.render("login.html", **p)
            else:
                self.login("user", user.key().id())
                self.redirect("/wall")
