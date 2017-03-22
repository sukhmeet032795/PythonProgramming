import json

from baseHandler.models import BaseHandler
from userHandler.models import User
from blogHandler.models import *
from loginHandler.views import *
from baseHandler.views import *
from userHandler.views import *

# Creating a new Blog Entry
class NewPost(BaseHandler):

    @loginRequired
    def get(self, userId, user_logged_in):

        if not user_logged_in:
            self.redirect("/login")

        userObj = User.getUser(int(userId))
        p = { "user" : userObj}
        self.render("newBlog.html", **p)

    @loginRequired
    def post(self, userId, user_logged_in):

        if not user_logged_in:
            self.redirect("/login")

        userObj = User.getUser(int(userId))

        title = self.request.get("title")
        subject = self.request.get("subject")

        p = { "title" : title, "subject" : subject, "user" : userObj }
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

            user = User.by_id(int(userId))

            blog = Blog(title = title, subject = subject, created_by = user)
            blog.put()

            return self.redirect("/blog/" + str(blog.key().id()))

# Editing a Blog Entry
class editBlog(BaseHandler):

    @loginRequired
    def get(self, blogId = None, userId = None, user_logged_in = None):

        if not user_logged_in:
            self.redirect("/login")

        userObj = User.getUser(userId)

        if not blogId:
            self.render("newBlog.html", user = userObj)

        else:
            blog = Blog.getBlog(int(blogId))
            p = { "id" : int(blogId), "title" : blog.title, "subject" : blog.subject, "user" : userObj}
            self.render("newBlog.html", **p)

    @loginRequired
    def post(self, blogId = None, userId = None, user_logged_in = None):

        if not user_logged_in:
            self.redirect("/login")

        userObj = User.getUser(userId)

        title = self.request.get("title")
        subject = self.request.get("subject")

        p = { "id" : blogId, "title" : title, "subject" : subject, "user" : userObj }
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

            user = User.by_id(int(userId))

            if not blogId:
                blog = Blog(title = title, subject = subject, created_by = user)
            else:
                blog = Blog.getBlog(int(blogId))
                blog.title = title
                blog.subject = subject
            blog.put()

            return self.redirect("/blog/" + str(blog.key().id()))

# Showing Blogs
class showBlog(BaseHandler):

    @loginRequired
    def get(self, blogId = None, userId = None, user_logged_in = None):

        if not user_logged_in:
            self.redirect("/login")

        blog = Blog.getBlog(int(blogId))

        if not blog:
            return self.redirect("/wall")

        checkLike = 0
        checkUser = 0
        userObj = User.getUser(userId)
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

                commentObj = { "id" : int(commentId), "content" : comment.content.encode("utf-8") , "name" : userName.encode("utf-8"), "userComment" : int(userComment) }
                comments.append(commentObj)

        bloguser = User.by_id(blog.created_by.key().id())
        blogUserName = bloguser.firstname + " " + bloguser.lastname

        render_text = blog.subject.replace("\n", "<br>")
        blogObj = { "title" : blog.title , "created" : blog.created, "id" : int(blog.key().id()), "comments" : comments, "likeStatus" : checkLike, "render_text" : render_text, "likes" : blog.likes, "user" : checkUser, "name" : blogUserName}

        self.render("blog.html", blog = blogObj, user = userObj)

#Liking a Blog Entry
class likeBlog(BaseHandler):

    @loginRequired
    def post(self, userId = None, user_logged_in = None):

        if not user_logged_in:
            msg = "nouser"
            status = "error"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        blogId = self.request.get("blogId")
        blog = Blog.getBlog(blogId)

        user = User.by_id(userId)
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

#Comment on a Blog
class commentBlog(BaseHandler):

    @loginRequired
    def post(self, userId = None, user_logged_in = None):

        if not user_logged_in:
            msg = "nouser"
            status = "error"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        user = User.by_id(userId)
        status = self.request.get("status")

        if status == "updateComment":
            id = self.request.get("id")
            content = self.request.get("content")

            comment = Comment.getComment(int(id))
            comment.content = content
            comment.put()

            msg = "updated"
            status = "success"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        blogId = self.request.get("blogId")
        blog = Blog.getBlog(blogId)

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

                checkUserComment = ((blog.created_by.key().id() == int(userId)) or (comment.created_by.key().id() == int(userId)))

                if not checkUserComment:
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

#Deleting a Blog
class deleteBlog(BaseHandler):

    @loginRequired
    def post(self, userId = None, user_logged_in = None):

        if not user_logged_in:
            msg = "nouser"
            status = "error"
            response = {"status": status, "msg": msg}
            return self.write(json.dumps(response))

        blogId = self.request.get("blogId")

        blog = Blog.getBlog(blogId)
        user = User.by_id(userId)

        if blog and user:

            if blog.created_by.key().id() != int(userId):
                msg = "otheruser"
                status = "error"
                response = {"status": status, "msg": msg}
                return self.write(json.dumps(response))

            comments = blog.comments
            for comment in comments:
                commentObj = Comment.getComment(int(comment))
                commentObj.delete()

            blog.delete()
            msg = "blogDeleted"
            status = "success"

        response = {"status": status, "msg": msg}
        return self.write(json.dumps(response))