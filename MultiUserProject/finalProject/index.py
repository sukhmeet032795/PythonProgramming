import webapp2
import os
import hashlib
import hmac
import jinja2
import json

from baseHandler.models import *
from userHandler.models import *
from userHandler.views import *
from signupHandler.models import *
from loginHandler.models import *
from blogHandler.models import *
from blogHandler.views import *

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Home(BaseHandler):

    def get(self):
        allBlogs = Blog.all().order("-created")

        userId = self.getLoggedInUser()

        userObj = User.getUser(userId)
        blogObjs = []

        for blog in allBlogs:

            checkLike = 0
            checkUser = 0
            user = None

            if userId:
                user = User.by_id(userId)

                if int(userId) in blog.likes:
                    checkLike = 1

                if blog.created_by.key().id() == user.key().id():
                    checkUser = 1

            comments = []
            allComments = blog.comments
            comments = commentHelper(allComments, user)

            bloguser = User.by_id(blog.created_by.key().id())
            blogUserName = bloguser.firstname + " " + bloguser.lastname

            render_text = blog.subject.replace('\n', '<br>')
            blogObj = { "title" : blog.title , "created" : blog.created, "id" : int(blog.key().id()), "comments" : comments, "likeStatus" : checkLike, "render_text" : render_text, "likes" : blog.likes, "user" : checkUser, "name" : blogUserName}
            blogObjs.append(blogObj)

        self.render("index.html", blogs = blogObjs, user = userObj)

class UserWall(BaseHandler):

    @loginRequired
    def get(self, userId = None, user_logged_in = None):

        if not user_logged_in:
            return self.redirect("/login")

        userObj = User.getUser(userId)
        user = User.by_id(userId)
        allBlogs = Blog.all().filter("created_by", user.key())
        blogObjs = []

        for blog in allBlogs:

            checkLike = 0
            checkUser = 1

            comments = []
            allComments = blog.comments
            comments = commentHelper(allComments, user)

            blogUserName = user.firstname + " " + user.lastname

            render_text = blog.subject.replace("\n", "<br>")
            blogObj = { "title" : blog.title , "created" : blog.created, "id" : int(blog.key().id()), "comments" : comments, "likeStatus" : checkLike, "render_text" : render_text, "likes" : blog.likes, "user" : checkUser, "name" : blogUserName}
            blogObjs.append(blogObj)

        self.render("index.html", blogs = blogObjs, user = userObj)

app = webapp2.WSGIApplication([("/", Home),
                               ("/wall", UserWall),
                               ("/newPost", NewPost),
                               ("/signup", Signup),
                               ("/login", Login),
                               ("/logout", Logout),
                               ("/blog/(\d+)", showBlog),
                               ("/likeBlog", likeBlog),
                               ("/commentBlog", commentBlog),
                               ("/deleteBlog", deleteBlog),
                               ("/checkUser", checkUser),
                               ("/editBlog/(\d+)", editBlog),
                              ])