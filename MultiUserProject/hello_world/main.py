import webapp2

form_get = """
<form action="/testform">
    <input name="q">
    <input type="submit">
</form>
"""

form_post = """
<form method="post" action="/testform">
    <input name="q">
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("Hello People!!!")

class FormHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(form_post)

class TestHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get("q")
        self.response.out.write(q)
        # self.response.headers['Content-Type'] = "text/plain"
        # self.response.out.write(self.request)

    def post(self):
        q = self.request.get("q")
        self.response.out.write(q)

app = webapp2.WSGIApplication([( '/', MainPage),
                               ('/form', FormHandler),
                               ('/testform', TestHandler)],
                                debug = True)