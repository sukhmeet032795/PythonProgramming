import os
import webapp2
import hashlib
import hmac
import jinja2
import re
import string
import random

from google.appengine.ext import db

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir),
                                autoescape = True)

# userid encryption for cookies

secret = ";P^#?j6G>&/Uk_A.MC\B2,sX$AjS9L$]HprQwLpx8}T=T+-"

def make_secure_hash(val):
    return "%s|%s" % (str(val), hmac.new(secret.encode('utf-8'), str(val).encode('utf-8')).hexdigest())

def check_secure_hash(hash):
    val = hash.split("|")[0]
    if (hash == make_secure_hash(val)):
        return True
    return False

#################################

# password encryption

def make_salt():
    return "".join(random.choice(string.ascii_letters) for x in range(5))

def make_pw_hash(name, pwd, salt = None):
    if not salt:
        salt = make_salt()
    return "%s,%s" % (salt, hashlib.md5(name.encode('utf-8') + pwd.encode('utf-8') + salt.encode('utf-8')).hexdigest())

def check_pw_hash(name, pwd, hash):
    salt = hash.split(",")[0]
    if hash == make_pw_hash(name, pwd, salt):
        return True
    return False

###############################

class User(db.Model):
    name = db.StringProperty(required  = True)
    email = db.StringProperty(required = False)
    pw_hash = db.StringProperty(required = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(int(uid))

    @classmethod
    def get_by_name(cls, name):
        user = User.all().filter("name", str(name)).get()
        return user

    @classmethod
    def register(cls, name, email, password):
        secure_pass = make_pw_hash(name, password)
        return User(name = name, email = email, pw_hash = secure_pass)

    @classmethod
    def login(cls, name, password):
        user = cls.get_by_name(name)
        if user:
            if check_pw_hash(name , password, user.pw_hash):
                return user

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.headers['Content Type'] = "text/html"
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def login(self, user):
        val = make_secure_hash(user.key().id())
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % ("user", val))

    def logout(self):
        self.response.headers.add_header("Set-Cookie", "user=; Path=/")

    def getuser(self):
        cookie = self.request.cookies.get("user")
        return cookie

class Register(Handler):

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

            u = User.get_by_name(username)

            if u:
                p['error_form'] = "Duplicate User Entry.Provide Valid Input"
                return self.render("index.html", **p)

            user = User.register(username, email, password)
            user.put()
            self.login(user)

            return self.redirect("/welcome")

class Logout(Handler):

    def get(self):
        self.logout()
        self.redirect('/')

class Home(Handler):

    def get(self):
        self.render("base.html")

class Login(Handler):

    def get(self):
        pass

class Welcome(Handler):

    def get(self):
        cookie = self.getuser()
        userid = cookie.split("|")[0]
        user = User.by_id(userid)
        self.render("welcome.html", username = user.name)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

app = webapp2.WSGIApplication([('/', Home),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', Welcome)
                              ])