import json
from userHandler.models import User
from baseHandler.models import BaseHandler

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

#Logging User Out
class Logout(BaseHandler):

    def get(self):
        self.logout("user")
        self.redirect("/")
