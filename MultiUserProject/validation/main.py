import webapp2
import cgi

form = """
<form method="post">
    <h2>Enter Your Birthday Details</h2>

    <label>
        Month
        <input type="text" name="month" value = "%(month)s">
    </label>
    <br>
    <br>
    <label>
        Day
        <input type="text" name="day" value = "%(day)s">
    </label>
    <br>
    <br>
    <label>
        Year
        <input type="text" name="year" value = "%(year)s">
    </label>
    <br>
    <br>
    <div style="color:red; font-size: 20px">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

months = ["January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"
        ]

month_abbr = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        short_mon = month[:3].lower()
        temp = month_abbr.get(short_mon)
        if(temp):
            if(temp.lower() == month.lower() or month.lower() == temp[:3].lower()):
                return temp
    return None

def valid_day(day):
    if day and day.isdigit():
        d = int(day)
        if (d > 0 and d < 32):
            return d
    return None

#Assume a year is valid if it is a number between 1900 and 2020.

def valid_year(year):
    if year and year.isdigit():
        y = int(year)
        if(y >= 1900 and y < 2021):
            return y
    return None

def escapeSequence(str):
    return cgi.escape(str, quote = True)

class MainPage(webapp2.RequestHandler):

    def write_form(self, error = "", month = "", day = "", year = ""):
        self.response.out.write(form % {'error' : error, 'month' : month, 'day' : day, 'year' : year})

    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.write_form()

    def post(self):
        user_month = self.request.get("month")
        user_day = self.request.get("day")
        user_year = self.request.get("year")

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not(month and day and year):
            self.write_form("Not a valid input, my friend....try again!!!",
                            escapeSequence(user_month),
                            escapeSequence(user_day),
                            escapeSequence(user_year))
        else:
            self.redirect("/thanks")

class ThankHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Yayyy!!! Your input is valid")

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/thanks', ThankHandler)],
                               debug = True)


