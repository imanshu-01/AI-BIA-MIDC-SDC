import turtle # Snake game using turtle graphics
import time # for controlling the game speed
import random # for random food placement

# ---------------- Screen Setup ----------------
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("lightgrey")
screen.setup(width=400, height=400)
screen.tracer(0)

# ---------------- Snake Head ----------------
head = turtle.Turtle()
head.shape("square")
head.color("purple")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ---------------- Snake Food ----------------
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# ---------------- Snake Body ----------------
segments = []

# ---------------- Score ----------------
score = 0

pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 170)
pen.write("Score: 0", align="center", font=("Arial", 14, "bold"))

# ---------------- Functions ----------------
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# ---------------- Keyboard Bindings ----------------
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# ---------------- Main Game Loop ----------------
while True:
    screen.update()

    # Border collision
    if abs(head.xcor()) > 190 or abs(head.ycor()) > 190:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for seg in segments:
            seg.goto(1000, 1000)
        segments.clear()
        score = 0
        pen.clear()
        pen.write("Score: 0", align="center", font=("Arial", 14, "bold"))

    # Food collision
    if head.distance(food) < 20:
        x = random.randint(-180, 180)
        y = random.randint(-180, 180)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("violet")
        new_segment.penup()
        segments.append(new_segment)

        score += 1
        pen.clear()
        pen.write(f"Score: {score}", align="center", font=("Arial", 14, "bold"))

    # Move body
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].pos())

    if segments:
        segments[0].goto(head.pos())

    move()

    # Body collision
    for seg in segments:
        if seg.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            for s in segments:
                s.goto(1000, 1000)
            segments.clear()
            score = 0
            pen.clear()
            pen.write("Score: 0", align="center", font=("Arial", 14, "bold"))

    time.sleep(0.15)
