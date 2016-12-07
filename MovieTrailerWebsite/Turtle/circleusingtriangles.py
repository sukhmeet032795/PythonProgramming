import turtle
import time

def createRhombus(b):

	b.forward(100)
	b.right(60)
	b.forward(100)
	b.right(120)
	b.forward(100)
	b.right(60)
	b.forward(100)
	b.right(120)

def createArt():
	
	brad = turtle.Turtle()
	window = brad.getscreen()
	window.bgcolor("black")

	brad.speed(0)
	# brad.begin_fill()
	brad.shape("turtle")
	brad.color("blue")

	brad.sety(-250)
	brad.left(90)
	brad.forward(300)
	brad.left(60)
	for i in range(1,73):
		createRhombus(brad)
		brad.right(5)

	# brad.fillcolor("violet")
	# brad.end_fill()
	window.exitonclick()

def createArt1():
	
	brady = turtle.Turtle()
	window = brady.getscreen()
	window.bgcolor("orange")

	brady.speed(0)
	brady.begin_fill()
	brady.shape("turtle")
	brady.color("blue", "yellow")

	brady.sety(-250)
	brady.left(90)
	brady.forward(300)
	brady.left(60)
	for i in range(1,37):
		createRhombus(brady)
		brady.right(10)

	brady.fillcolor("green")
	brady.end_fill()
	window.exitonclick()

createArt()
# createArt1()


