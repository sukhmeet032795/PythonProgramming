import webapp2
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.headers["Content Type"] = "text/html"
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
  title = db.StringProperty(required = True)
  art = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):

    def render_form(self, **params):
        self.render("homepage.html", **params)

    def get(self):
        getarts = db.GqlQuery("select * from Art order by created desc")
        p = {'title' : "", 'art' : "", 'error' : "", 'arts' : getarts}
        self.render_form(**p)

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title,art =  art)
            a.put()
            self.redirect("/")

        else:
            p = {'title' : title, 'art' : art, 'error' : "Oops...we require both title and art"}
            self.render("homepage.html", **p)

app = webapp2.WSGIApplication([('/', MainPage)
                              ])
