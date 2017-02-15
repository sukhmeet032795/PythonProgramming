import webapp2
import os
import hashlib
import hmac
import jinja2
import re
import random
import string
import json

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


#############Encryption Handling#############

#############Cookie Hash#############

secret_key = ",qLY5!RD06.w1onRFC$M8=w<-#M+DjvA,9<mB,*Yq#ZavEf.k`KZKP\2)V:(.,E"

def make_cookie_hash(userId):
    return ("%s|%s" % (str(userId), hmac.new( str(userId).encode("utf-8") + secret_key.encode("utf-8") ).hexdigest()))

def check_cookie_hash(hash):

    if not hash:
        return False

    userId = hash.split("|")[0]
    if hash == make_cookie_hash(userId):
        return True
    return False

#######################################

#############Password Hash#############

def generate_salt():
    return "".join(random.choice(string.ascii_letters) for x in range(5))

def make_pw_hash(username, pwd, salt = None):

    if not salt:
        salt = generate_salt()
    return "%s,%s" % (salt, hashlib.sha256(salt.encode("utf-8") + username.encode("utf-8") + pwd.encode("utf-8")).hexdigest())

def check_pw_hash(username, pwd, hash):

    if not hash:
        return False

    salt = hash.split(",")[0]
    if make_pw_hash(username, pwd, salt) == hash:
        return True
    return False

#######################################

#############Encryption Handling Ends#############


#############Main Handler#############

class BlogHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.headers["Content Type"] = "text/html"
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def login(self, name, val):
        cookie_hash = make_cookie_hash(val)
        self.response.headers.add_header("Set-Cookie", "%s=%s; Path=/" % (name, cookie_hash))

    def logout(self, name):
        self.response.headers.add_header("Set-Cookie", "%s=; Path=/" % (name))

    def get_cookie_hash(self, name):
        return self.request.cookies.get(str(name))

    def get_user_id(self, hash):
        return hash.split("|")[0]

###########Main Handler Ends###########


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
                self.login("user", user.key().id())
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
                self.login("user", user.key().id())
                self.redirect("/newPost")

class Logout(BlogHandler):

    def get(self):
        self.logout("user")
        self.redirect("/")

# Blog Module

class Comment(db.Model):
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    created_by = db.ReferenceProperty(User)

    @classmethod
    def getComment(cls, commentId):
        return cls.get_by_id(int(commentId))

class Blog(db.Model):
    title = db.StringProperty(required = True)
    subject = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now = True)
    likes = db.ListProperty(int)
    comments = db.ListProperty(int)
    created_by = db.ReferenceProperty(User)

    def render(self):
        self._render_text = self.subject.replace('\n', '<br>')
        return render_str("post.html", blog = self)

    @classmethod
    def getBlog(cls, blogId):
        return cls.get_by_id(int(blogId))

class Home(BlogHandler):

    def get(self):
        allBlogs = Blog.all().order("-created")

        cookie_hash = self.get_cookie_hash("user")
        userId = None

        if check_cookie_hash(cookie_hash):
            userId = self.get_user_id(cookie_hash)
        blogObjs = []

        for blog in allBlogs:

            check = 0
            if userId in blog.likes:
                check = 1

            comments = []

            allComments = blog.comments
            if (len(allComments) != 0):
                allComments.reverse()
                for commentId in allComments:
                    comment = Comment.getComment(commentId)
                    user = User.by_id(comment.created_by.key().id())
                    userName = user.firstname + " " + user.lastname
                    commentObj = { "id" : int(commentId), "content" : comment.content.encode("utf-8") , "name" : userName.encode("utf-8") }
                    comments.append(commentObj)

            render_text = blog.subject.replace("\n", "<br>")
            blogObj = { "title" : blog.title , "created" : blog.created, "id" : int(blog.key().id()), "comments" : comments, "likeStatus" : check, "render_text" : render_text, "likes" : blog.likes}
            blogObjs.append(blogObj)

        self.render("index.html", blogs = blogObjs)

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
            return self.render("newBlog.html", **p)
        else:

            cookie_hash = self.get_cookie_hash("user")
            if not check_cookie_hash(cookie_hash):
                return self.redirect("/login")
            else:
                userId = self.get_user_id(cookie_hash)

            user = User.by_id(userId)
            blog = Blog(title = title, subject = subject, created_by = user)
            blog.put()

            return self.redirect("/blog/" + str(blog.key().id()))

class showBlog(BlogHandler):

    def get(self, blogId):
        blog = Blog.getBlog(blogId)

        cookie_hash = self.get_cookie_hash("user")
        userId = None

        if check_cookie_hash(cookie_hash):
            userId = self.get_user_id(cookie_hash)

        check = 0
        if userId in blog.likes:
            check = 1

        comments = []

        for commentId in blog.comments:
            comment = Comment.getComment(commentId)
            user = User.by_id(comment.created_by.key().id())
            userName = user.firstname + " " + user.lastname
            commentObj = { "id" : int(commentId) , "content" : comment.content.encode("utf-8") , "name" : userName.encode("utf-8") }
            comments.append(commentObj)

        render_text = blog.subject.replace("\n", "<br>")
        blogObj = { "title" : blog.title , "created" : blog.created, "id" : int(blog.key().id()), "comments" : comments, "likeStatus" : check, "render_text" : render_text, "likes" : blog.likes}
        print (blogObj)
        self.render("blog.html", blog = blogObj)

class likeBlog(BlogHandler):

    def post(self):
        blogId = self.request.get("blogId")
        blog = Blog.getBlog(blogId)
        cookie_hash = self.get_cookie_hash("user")
        user = None

        if check_cookie_hash(cookie_hash):
            userId = self.get_user_id(cookie_hash)
            user = User.by_id(userId)

        if not user:
            msg = "nouser"
            status = "error"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        userId = user.key().id()
        blogUserId = blog.created_by.key().id()
        likes_count = len(blog.likes)

        if (blogUserId == userId):
            msg = "selflike"
            status = "error"

        elif blog and user:

            if userId in blog.likes:
                blog.likes.remove(int(userId))
                blog.put()
                msg = "unliked"
                status = "success"

            else:
                blog.likes.append(int(user.key().id()))
                blog.put()
                msg = "liked"
                status = "success"

            likes_count = len(blog.likes)

        response = {"status": status, "msg": msg, "count" : str(likes_count)}
        return self.write(json.dumps(response))

class commentBlog(BlogHandler):

    def post(self):
        blogId = self.request.get("blogId")
        status = self.request.get("status")

        blog = Blog.getBlog(blogId)
        cookie_hash = self.get_cookie_hash("user")
        user = None

        if check_cookie_hash(cookie_hash):
            userId = int(self.get_user_id(cookie_hash))
            user = User.by_id(userId)

        if not user:
            msg = "nouser"
            status = "error"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        if status == "createComment":

            content = self.request.get("comment")
            if blog and user:

                comment = Comment(content = content, created_by = user)
                comment.put()
                blog.comments.append(int(comment.key().id()))
                blog.put()

                name = user.firstname + " " + user.lastname

                commentObj = { "id" : int(comment.key().id()), "content" : content, "name" : name }

                msg = "commented"
                status = "success"

            response = {"status": status, "msg": msg, "comment" : commentObj}
            return self.write(json.dumps(response))

        elif status == "deleteComment":

            commentId = int(self.request.get("commentId"))
            if blog and user:

                comment = Comment.getComment(commentId)

                if blog.created_by.key().id() != userId:
                    msg = "otheruser"
                    status = "error"
                    response = {"status": status, "msg": msg}
                    return self.write(json.dumps(response))

                comment.delete()
                blog.comments.remove(int(commentId))
                blog.put()
                msg = "uncommented"
                status = "success"

            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

class deleteBlog(BlogHandler):

    def post(self):
        blogId = self.request.get("blogId")

        blog = Blog.getBlog(blogId)
        cookie_hash = self.get_cookie_hash("user")
        user = None

        if check_cookie_hash(cookie_hash):
            userId = int(self.get_user_id(cookie_hash))
            user = User.by_id(userId)

        if not user:
            msg = "nouser"
            status = "error"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        if blog and user:

            if blog.created_by.key().id() != userId:
                msg = "otheruser"
                status = "error"
                response = {"status": status, "msg": msg}
                return self.write(json.dumps(response))

            blog.delete()
            msg = "blogDeleted"
            status = "success"

        response = {"status": status, "msg": msg}
        return self.write(json.dumps(response))

app = webapp2.WSGIApplication([("/", Home),
                               ("/newPost", NewPost),
                               ("/signup", Signup),
                               ("/login", Login),
                               ("/logout", Logout),
                               ("/blog/(\d+)", showBlog),
                               ("/likeBlog", likeBlog),
                               ("/commentBlog", commentBlog),
                               ("/deleteBlog", deleteBlog),
                              ])