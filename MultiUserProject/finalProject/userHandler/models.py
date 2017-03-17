import random
import string
import hashlib
import os
import jinja2

from google.appengine.ext import db
from loginHandler.views import *

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class User(db.Model):
    firstname = db.StringProperty(required  = True)
    lastname = db.StringProperty(required  = True)
    username = db.StringProperty(required  = True)
    email = db.StringProperty(required  = False)
    pw_hash = db.StringProperty(required  = True)

    @classmethod
    def by_id(cls, id):
        return User.get_by_id(int(id))

    @classmethod
    def by_username(cls, username = None):
        return User.all().filter("username", username).get()

    @classmethod
    def register(cls, fname, lname, uname, email, password):
        pw_hash = make_pw_hash(uname, password)
        return User(firstname = fname,
                    lastname = lname,
                    username = uname,
                    email = email,
                    pw_hash = pw_hash)

    @classmethod
    def getUser(cls, userId):

        name = ""
        user = None
        checkLoggedInUser = 0
        if not userId:
            return None

        if userId:
            checkLoggedInUser = 1
            user = cls.by_id(userId)
            name = user.firstname + " " + user.lastname

        userObj = { "status" : checkLoggedInUser, "name" : name, "id" : userId }
        return userObj