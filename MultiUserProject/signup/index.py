import webapp2
import cgi
import os
import codecs
import re
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.headers['Content Type'] = "text/html"
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class signup(Handler):
    def get(self):
        self.render("index.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        cpassword = self.request.get("verify")
        email = self.request.get("email")

        params = {}

        params["username"] = username
        params["email"] = email

        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        error = False

        if not valid_username(username):
            params["error_username"] = "That's not a valid username."
            error = True

        if not valid_email(email):
            params["error_email"] = "That's not a valid email."
            error = True

        if not valid_password(password):
            params["error_password"] = "That wasn't a valid password."
            error = True
        elif password != cpassword:
            params["error_verify"] = "Your passwords didn't match."
            error = True

        if error:
            self.render("index.html", **params)
        else:
            self.redirect("/welcome?username=" + username)

class welcome(Handler):
    def get(self):
        name = self.request.get("username")
        self.render("welcome.html", name = name)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

app = webapp2.WSGIApplication([('/signup', signup),
                               ('/welcome', welcome)
                              ])


