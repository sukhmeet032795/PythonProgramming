import re
import jinja2
import os

from baseHandler.models import BaseHandler
from userHandler.models import User
from signupHandler.views import *
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Signup(BaseHandler):

    def get(self):
        userId = self.getLoggedInUser()

        if userId:
            self.redirect("/wall")
        else:
            self.render("signup.html", user = 0)

    def post(self):
        fname = self.request.get("firstname")
        lname = self.request.get("lastname")
        uname = self.request.get("username")
        email = self.request.get("email")
        password = self.request.get("password")
        cpassword = self.request.get("cpassword")

        p = { "firstname" : fname, "lastname" : lname, "username" : uname, "email" : email }
        p["user"] = 0
        error = False

        if not valid_name(fname):
            p["error_firstname"] = "Not a Valid FirstName"
            error = True

        if not valid_name(lname):
            p["error_lastname"] = "Not a Valid LastName"
            error = True

        if not valid_username(uname):
            p["error_username"] = "Not a UserName"
            error = True

        if not valid_email(email):
            p["error_email"] = "Not a Valid Email"
            error = True

        if not valid_password(password):
            p["error_password"] = "Not a Valid Password"
            error = True
        elif password != cpassword:
            p["error_cpassword"] = "Passwords Don't Match"
            error = True

        if error:
            return self.render("signup.html", **p)
        else:

            user = User.by_username(uname)
            p["user"] = user

            if user:
                p["error_username"] = "UserName is not available"
                return self.render("signup.html", **p)
            else:
                user = User.register(fname, lname, uname, email, password)
                user.put()
                self.login("user", user.key().id())
                self.redirect("/newPost")