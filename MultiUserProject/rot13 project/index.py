import os
import jinja2
import cgi
import webapp2
import codecs

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.headers['Content Type'] = "text/html"
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class rot13(Handler):
    def get(self):
        self.render("index.html", text = "")

    def post(self):
        encoded = ""
        text = self.request.get("text")
        if text:
            encoded = codecs.encode(text, "rot-13")
        return self.render("index.html", text = encoded)

class MainPage(Handler):
    def get(self):
        self.render("main.html")

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13', rot13)
                              ])
