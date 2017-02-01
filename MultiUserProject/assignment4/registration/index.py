import os
import webapp2
import hashlib
import hmac
import jinja2
import re

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir),
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

class home(Handler):
    def get(self):
        self.render("index.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        cpassword = self.request.get("cpassword")
        email = self.request.get("email")

        p = {'username' : username, 'email' : email}
        error = False

        if not valid_username(username):
            p['error_username'] = "Not a valid username"
            error = True

        if not valid_email(email):
            p['error_email'] = "Not a valid email"
            error = True

        if not valid_password(password):
            p['error_password'] = "Not a valid password"
            error = True
        elif (password != cpassword):
            p['error_cpassword'] = "Passwords do not match"
            error = True

        if error:
            return self.render("index.html", **p)
        else:
            return self.render("welcome.html", username = username)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

app = webapp2.WSGIApplication([('/', home)
                              ])