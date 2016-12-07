import webbrowser

class Movie(object):

	title = ''
	url = ''
	story = ''
	reviews = []
	poster = ''

	def __init__(self, movie_title, movie_url, movie_storyLine, movie_reviews, movie_posterUrl):

		self.title = movie_title
		self.url = movie_url
		self.story = movie_storyLine
		self.poster = movie_posterUrl

		for review in movie_reviews:
			self.reviews.append(review)

	def showTitle(self):
		return self.title

	def showStory(self):
		return self.story

	def showReviews(self):
		return self.reviews

	def showPoster(self):
		webbrowser.open(self.poster)	
		return self.poster
		
	def showTrailer(self):
		webbrowser.open(self.url)
		return self.url							

