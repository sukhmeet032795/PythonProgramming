import media
import fresh_tomatoes

bajiraoMastani = media.Movie(

		"Bajirao Mastani",
		"https://www.youtube.com/watch?v=eHOc-4D7MjY",
		"An account of the romance between the Maratha general, Baji Rao I and Mastani, a Muslim princess.",
		["A fantastic and classic epic romance", "Well-Made, Well-Acted Motion-Picture!", "surreal direction, exemplary CGI and commendable performances"],
		"https://upload.wikimedia.org/wikipedia/en/5/52/Bajirao_Mastani_Poster_2.jpg"
	)

pink = media.Movie(

		"Pink",
		"https://www.youtube.com/watch?v=AL2TShb6fFs",
		"When three young women are implicated in a crime; a retired lawyer steps forward to help them clear their names.",
		["Excellent, intense & gripping courtroom drama!!", "Dyeing our conscience", "Cinema's Pink Revolution"],
		"https://upload.wikimedia.org/wikipedia/en/a/ae/Pinkmovieposter.jpg"
	)

zindagiNaMilegiDubara = media.Movie(

		"Zindagi Na Milegi Dubara",
		"https://www.youtube.com/watch?v=ifIBOKCfjVs",
		"Three friends decide to turn their fantasy vacation into reality after one of their number becomes engaged.",
		["Excellent Movie", "Mind Blowing Stuff", "Mental Buoys Rockzzzz..", "Perfect summer movie about the journey of Life"],
		"https://upload.wikimedia.org/wikipedia/en/3/3d/Zindaginamilegidobara.jpg"
	)

queen = media.Movie(

		"Queen",
		"https://www.youtube.com/watch?v=KGC6vl3lzf0",
		"A Delhi girl from a traditional family sets out on a solo honeymoon after her marriage gets cancelled.",
		["This 'queen' will surely rule your hearts!", "This QUEEN is ROYAL in every way!", "Queen is soul stirring", "Queen of Hearts!!"],
		"https://upload.wikimedia.org/wikipedia/en/4/45/QueenMoviePoster7thMarch.jpg"
	)

jabWeMet = media.Movie(

		"Jab We Met",
		"https://www.youtube.com/watch?v=T_Fy0qlgfo4",
		"A depressed wealthy businessman finds his life changing after he meets a spunky and care-free young woman.",
		["Lovely, simple and full of life", "Excellent Movie, Great Plot", "Totally Entertaining", "A Funny Little Film"],
		"https://upload.wikimedia.org/wikipedia/en/9/9f/Jab_We_Met_Poster.jpg"
	)

munnaBhai = media.Movie(

		"Munna Bhai M.B.B.S.",
		"https://www.youtube.com/watch?v=6lCGvu-hwX4",
		"A gangster sets out to fulfill his father's dream of becoming a doctor.",
		["Excellent Tapori Movie", "Laughter Guaranteed!!", "Real nice comedy", "A Laugh Riot!"],
		"https://upload.wikimedia.org/wikipedia/en/1/19/Munna_Bhai_M.B.B.S.%2C_2003_Hindi_film_poster.jpg"
	)

toystory = media.Movie(
		
		"ToyStory", 
		"https://www.youtube.com/watch?v=4KPTXpQehio", 
		"A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.", 
		["The adventure takes off!", "Guts of steel", "Buzz off!", "Oooh...3-D"], 
		"https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg"
	)

avatar = media.Movie(

		"Avatar",
		"https://www.youtube.com/watch?v=cRdxXPV9GNQ",
		"A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
		["Return to Pandora", "Enter the World", "Worth watching", "Eye-popping spectacle of conflict"],
		"https://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg"
	)

movies = [bajiraoMastani, pink, zindagiNaMilegiDubara, queen, jabWeMet, munnaBhai, toystory, avatar]

fresh_tomatoes.open_movies_page(movies)
