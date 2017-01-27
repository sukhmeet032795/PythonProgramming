import webapp2
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.headers["Content Type"] = "text/html"
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class mainPage(Handler):

    def get(self):
        blogs = db.GqlQuery("select * from Blogs order by created desc")
        self.render("allBlogs.html", blogs = blogs)

    # def post(self):

class Blogs(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", blog = self)

class newpost(Handler):

    def render_form(self):
        p = {'subject' : "", 'content' : "", 'error' : ""}
        self.render("form.html", **p)

    def get(self):
        self.render_form()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            b = Blogs(subject = subject, content = content)
            b.put()
            id = b.key().id()
            self.redirect("/blogs/"+str(id))

        else:
            p = {'subject' : "", 'content' : "", 'error' : ""}
            self.render("form.html", **p)

class showBlog(Handler):

    def get(self, blogId):
        b = db.Key.from_path('Blogs', int(blogId))
        blog = db.get(b)

        if not blog:
            self.render(404)
        else:
            self.render("blog.html", blog = blog)

app = webapp2.WSGIApplication([("/blogs", mainPage),
                               ("/blogs/newpost", newpost),
                               ("/blogs/(\d+)", showBlog)
                              ])