import turtle

t = turtle.Turtle()
window = t.getscreen()
window.bgcolor("black")
t.speed(0)
t.color("blue")
t.shape("turtle")

print (t.position())

def createS(t):

	t.pendown()
	t.forward(10)
	for i in range(1, 34):
	    t.right(2)
	    t.forward(1)

	t.left(180)
	t.penup()
	for i in range(1, 34):
	    t.left(2)
	    t.forward(1)
	t.forward(10)    

	t.pendown()    
	for i in range(1, 91):
	    t.left(2)
	    t.forward(1)

	t.forward(10)    
	for i in range(1, 91):
	    t.right(2)
	    t.forward(1)

	t.forward(10)    
	for i in range(1, 34):
	    t.right(2)
	    t.forward(1)	    

createS(t)

t.penup()
t.setposition(120.00 , 0.00)
t.right(115)

createS(t)

t.penup()
t.setposition(220.00, -110.00)

window.exitonclick()    

    
