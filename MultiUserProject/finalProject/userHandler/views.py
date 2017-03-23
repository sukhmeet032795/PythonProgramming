import json
import webapp2
from userHandler.models import User
from baseHandler.views import *

#Checking the Presence of User
class checkUser(BaseHandler):

    def get(self):

        userId = self.getLoggedInUser()
        userObj = User.getUser(userId)

        if not userObj:
            msg = "nouser"
            status = "error"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        else:
            msg = "user"
            status = "success"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

def loginRequired(func):
    def check_login(self, *args, **kw):
        cookie_hash = self.request.cookies.get("user")
        userId = None
        user_logged_in = False

        if check_cookie_hash(cookie_hash):
            userId = cookie_hash.split("|")[0]
            user_logged_in = True

        return func(self, userId = userId, user_logged_in = user_logged_in, *args, **kw)
    return check_login

#Logging User Out
class Logout(BaseHandler):

    def get(self):
        self.logout("user")
        self.redirect("/")
