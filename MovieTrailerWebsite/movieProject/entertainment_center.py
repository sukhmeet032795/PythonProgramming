import media

toystory = media.Movie(
		
		"ToyStory", 
		"https://www.youtube.com/watch?v=4KPTXpQehio", 
		"Imagination runs rampant when toys become mobile when not watched. Two toys, Woody and Buzz Lightyear despise each other like no other. But, when the toys are separated from their home, a truce is formed between them all in an effort to journey home.", 
		['The adventure takes off!', 'Guts of steel', 'Buzz off!', 'Oooh...3-D'], 
		"http://www.imdb.com/title/tt0114709/mediaviewer/rm3813007616"
	)

avatar = media.Movie(

		"Avatar",
		"https://www.youtube.com/watch?v=cRdxXPV9GNQ",
		"A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
		['Return to Pandora', 'Enter the World', 'Worth watching', 'Eye-popping spectacle of conflict'],
		"http://www.imdb.com/title/tt0499549/mediaviewer/rm843615744"
	)

print (toystory.story)
print (avatar.story)
