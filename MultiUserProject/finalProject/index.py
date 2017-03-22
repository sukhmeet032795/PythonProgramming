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
            if (len(allComments) != 0):
                allComments.reverse()
                for commentId in allComments:
                    comment = Comment.getComment(commentId)
                    commentUser = User.by_id(comment.created_by.key().id())
                    userName = commentUser.firstname + " " + commentUser.lastname

                    userComment = 0

                    if user:
                        if commentUser.key().id() == user.key().id():
                            userComment = 1

                    commentObj = { "id" : int(commentId), "content" : comment.content.encode('utf-8') , "name" : userName.encode('utf-8'), "userComment" : int(userComment) }
                    comments.append(commentObj)

            bloguser = User.by_id(blog.created_by.key().id())
            blogUserName = bloguser.firstname + " " + bloguser.lastname

            render_text = blog.subject.replace('\n', '<br>')
            blogObj = { "title" : blog.title , "created" : blog.created, "id" : int(blog.key().id()), "comments" : comments, "likeStatus" : checkLike, "render_text" : render_text, "likes" : blog.likes, "user" : checkUser, "name" : blogUserName}
            blogObjs.append(blogObj)

        self.render("index.html", blogs = blogObjs, user = userObj)

class UserWall(BaseHandler):

    def get(self):
        userId = self.getLoggedInUser()

        userObj = User.getUser(userId)
        blogObjs = []

        if not userObj:
            return self.redirect("/login")

        user = User.by_id(userId)
        allBlogs = Blog.all().filter("created_by", user.key())

        for blog in allBlogs:

            checkLike = 0
            checkUser = 1

            comments = []

            allComments = blog.comments
            if (len(allComments) != 0):
                allComments.reverse()
                for commentId in allComments:
                    comment = Comment.getComment(commentId)
                    commentUser = User.by_id(comment.created_by.key().id())
                    userName = commentUser.firstname + " " + commentUser.lastname

                    userComment = 0

                    if user:
                        if commentUser.key().id() == user.key().id():
                            userComment = 1

                    commentObj = { "id" : int(commentId), "content" : comment.content.encode("utf-8") , "name" : userName.encode("utf-8"), "userComment" : int(userComment) }
                    comments.append(commentObj)

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