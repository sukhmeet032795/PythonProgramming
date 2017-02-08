import webapp2
import os
import hashlib
import hmac
import jinja2
import re

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
        return User.all().filter(username = username).get()

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
            self.render("signup.html", **p)

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
                               ("/signup", Signup)
                              ])