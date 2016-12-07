import turtle
import time

def createSquare(b):

	for i in range(1,5):
		b.forward(100)
		b.left(90)

def createArt():
	
	brad = turtle.Turtle()
	window = brad.getscreen()
	window.bgcolor("black")

	brad.speed(0)
	brad.begin_fill()
	brad.shape("turtle")
	brad.color("blue", "red")

	for i in range(1,361):
		createSquare(brad)
		brad.right(1)

	brad.fillcolor("violet")
	brad.end_fill()
	window.exitonclick()

def createArt1():
	
	brady = turtle.Turtle()
	window = brady.getscreen()
	window.bgcolor("red")

	brady.speed(0)
	brady.begin_fill()
	brady.shape("turtle")
	brady.color("blue", "yellow")

	for i in range(1,361):
		createSquare(brady)
		brady.right(1)

	brady.fillcolor("green")
	brady.end_fill()
	window.exitonclick()

createArt()
createArt1()


