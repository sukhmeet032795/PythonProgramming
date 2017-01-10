import webapp2

form = """
<form action="http://www.google.com/search">
    <input name="q">
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("Hello People!!!")

class MainPage1(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(form)

app = webapp2.WSGIApplication([( '/', MainPage), ('/form', MainPage1)],
                                debug = True)