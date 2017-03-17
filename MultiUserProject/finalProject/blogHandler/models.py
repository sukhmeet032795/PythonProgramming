import jinja2
import os

from baseHandler.models import BaseHandler
from userHandler.models import User
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


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

