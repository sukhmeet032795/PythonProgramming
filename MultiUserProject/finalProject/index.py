import webapp2
import os
import hashlib
import hmac
import jinja2
import re
import random
import string

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BlogHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.headers["Content Type"] = "text/html"
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


# User Registration and Login Module

######################

USER_RE = re.compile(r"^[a-zA-Z]{3,20}$")
def valid_name(name):
    return name and USER_RE.match(name)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

######################

def generate_salt():
    return "".join(random.choice(string.ascii_letters) for x in range(5))

def make_pw_hash(username, pwd, salt = None):

    if not salt:
        salt = generate_salt()
    return "%s,%s" % (salt, hashlib.sha256(salt.encode("utf-8") + username.encode("utf-8") + pwd.encode("utf-8")).hexdigest())

def check_pw_hash(username, pwd, hash):

    salt = hash.split(",")[0]
    if make_pw_hash(username, pwd, salt) == hash:
        return True
    return False

######################

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

class Signup(BlogHandler):

    def get(self):
        self.render("signup.html")

    def post(self):
        fname = self.request.get("firstname")
        lname = self.request.get("lastname")
        uname = self.request.get("username")
        email = self.request.get("email")
        password = self.request.get("password")
        cpassword = self.request.get("cpassword")

        p = { "firstname" : fname, "lastname" : lname, "username" : uname, "email" : email }
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

            if user:
                p["error_username"] = "UserName is not available"
                return self.render("signup.html", **p)
            else:
                user = User.register(fname, lname, uname, email, password)
                user.put()
                self.redirect("/newPost")

class Login(BlogHandler):

    def get(self):
        self.render("login.html")

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
            return self.render("login.html", **p)
        else:

            if not check_pw_hash(username, password, user.pw_hash):
                p["error_form"] = "UserName/Password combination is invalid"
                return self.render("login.html", **p)
            else:
                self.redirect("/newPost")


# Blog Module

class Blog(db.Model):
    title = db.StringProperty(required = True)
    subject = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now = True)
    created_by = db.ReferenceProperty(User)

    @staticmethod
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("blog.html", blog = self)

class Home(BlogHandler):

    def get(self):
        blogs = Blog.all()
        self.render("index.html", blogs = blogs)

class NewPost(BlogHandler):

    def get(self):
        self.render("newBlog.html")

    def post(self):
        title = self.request.get("title")
        subject = self.request.get("subject")

        p = { "title" : title , "subject" : subject }
        error = False

        if not title:
            p["error_title"] = "Title Is Not Valid"
            error = True

        if not subject:
            p["error_subject"] = "Subject Is Not Valid"
            error = True

        if error:
            self.render("newBlog.html", **p)

app = webapp2.WSGIApplication([("/", Home),
                               ("/newPost", NewPost),
                               ("/signup", Signup),
                               ("/login", Login),
                              ])