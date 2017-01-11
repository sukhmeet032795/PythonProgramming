import webapp2

form = """
<form method="post">
    <h2>Enter Your Birthday Details</h2>

    <label>
        Month
        <input type="text" name="month">
    </label>

    <label>
        Day
        <input type="text" name="day">
    </label>

    <label>
        Year
        <input type="text" name="year">
    </label>

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

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(form)

    def post(self):
        user_month = valid_month(self.request.get("month"))
        user_day = valid_day(self.request.get("day"))
        user_year = valid_year(self.request.get("year"))

        if not(user_month and user_day and user_year):
            self.response.out.write(form)
        else:
            self.response.out.write("Yayyy!!! Your input is valid")

app = webapp2.WSGIApplication([( '/', MainPage),
                              ],
                               debug = True)


