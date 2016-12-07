import webbrowser

class Movie(object):

	title = ''
	url = ''
	story = ''
	reviews = []

	def __init__(self, title, youtubeUrl, storyLine, reviews):

		self.title = title
		self.url = youtubeUrl
		self.story = storyLine

		for review in reviews:
			self.reviews.append(review)

	def showTitle(self):
		return self.title

	def showStory(self):
		return self.story

	def showReviews(self):
		return self.reviews
		
	def showTrailer(self):
		webbrowser.open(self.url)
		return self.url					

