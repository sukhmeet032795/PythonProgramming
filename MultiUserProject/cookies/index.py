import webapp2
import jinja2
import os
import hashlib
import hmac
import string
import random
from google.appengine.ext import db

SECRET = "sonu1995"

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir),
                                autoescape = True)

# def hash(s):
    # return hashlib.md5(s.encode('utf-8')).hexdigest()

def make_salt():
    return "".join(random.choice(string.ascii_letters) for x in range(5))

def hash_better(s):
    hmac.new(SECRET.encode('utf-8'), s.encode('utf-8')).hexdigest()

def make_secure_hash(s):
    salt = make_salt()
    return hashlib.sha256(salt.encode('utf-8') + s.encode('utf-8')).hexdigest()

# def make_secure_hash(s):
#     return ("%s|%s" % (s, hash_better(s)))

def check_hash(h):
    val = h.split("|")[0]
    if make_secure_hash(val) == h:
        return val
    return None

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.headers['Content Type'] = 'text/plain'
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template, **kw):
        self.write(self.render_str(template, **kw))

class baseHandler(Handler):
    def get(self):
        visits_hash = self.request.cookies.get('visits')
        visits = 0
        if visits_hash:
            visits_val = check_hash(visits_hash)
            if visits_val:
                visits = int(visits_val)
            else:
                visits = 0

        visits += 1
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % make_secure_hash(str(visits)))
        self.write("test - > %s" % visits)

app = webapp2.WSGIApplication([('/', baseHandler),])
