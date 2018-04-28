from tkinter import *
import random
import time

WIN_WIDTH = 600
WIN_HEIGHT = 600

#Array of directions to choose from
DIRECTIONS = ['U', 'R', 'D', 'L']

class Fruit:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20, fill = "red")

        self.spawn()

    def spawn(self):
        self.x_start = (random.randint(0,600))
        self.y_start = (random.randint(0,600))
        self.canvas.coords(self.id, self.x_start, self.y_start, self.x_start + 10, self.y_start + 10)
        self.position = self.canvas.coords(self.id)

    def collision_check(self, Head):
        if (self.position[0] - 10) <= Head.position[0] <= (self.position[0] + 10) and (self.position[3] - 10) <= Head.position[3] <= (self.position[3] + 10):
            Head.length += 1
            self.canvas.itemconfigure(Head.score_id, text = Head.length)
            print ("Fruit, Collision_Check: Score Updated")
            self.spawn()
            print ("Fruit, Collision_Check: New fruit spawned")
            Head.body.append(Body(self.canvas, Head.position))
            print("Fruit, Collision_Check: Appended new Body Object")
            self.speed += .25
            print ("Fruit, collision_check: Increased Speed")

    position = None
    x_start = None
    y_start = None
    speed = 2

class Falling_Fruit(Fruit):
    def draw(self):
        self.canvas.move(self.id, 0, self.speed)
        self.position = self.canvas.coords(self.id)
        if self.position[3] >= WIN_HEIGHT:
            self.spawn()

class Body:
    def __init__(self, canvas, last_pos):
        """ Initializes the Body objects of the snake """
        self.canvas = canvas

        self.id = canvas.create_oval(-20,-20,-10,-10, fill = "green")
        self.draw(last_pos)

    def draw(self, last_pos):
        """ Stores position values and moves body objects """
        self.last_position = self.position
        print ("Body, Draw: Last Position Set")

        self.position = self.canvas.coords(self.id)
        print ("Body, Draw: Position Set")

        self.canvas.coords(self.id, last_pos)
        print ("Body, Draw: Coordinates Set")

    position = None
    last__position = None


class Head:
    def __init__(self, canvas):
        """ Initializes the snake head object """
        self.canvas = canvas

        self.score_id = canvas.create_text(300,20,fill="darkblue",font="Times 20 italic bold", text=self.length)

        self.id = canvas.create_oval(10,10,20,20, fill = "green")

        self.x_start = (random.randint(0,600))
        self.y_start = (random.randint(0,600))

        self.canvas.coords(self.id, self.x_start, self.y_start, self.x_start + 10, self.y_start + 10)

        direction = DIRECTIONS[random.randint(0,3)]
        self.inside_window = True
        print ("Head, init: Snake Initialized")

        canvas.bind_all('<Up>', self.move_up)
        canvas.bind_all('<Right>', self.move_right)
        canvas.bind_all('<Down>', self.move_down)
        canvas.bind_all('<Left>', self.move_left)
        print ("Head, init: Controls Bound")

    def move_up(self, event):
        self.direction = DIRECTIONS[0]
        print ("DIR: UP")

    def move_right(self, event):
        self.direction = DIRECTIONS[1]
        print ("DIR: RIGHT")

    def move_down(self, event):
        self.direction = DIRECTIONS[2]
        print ("DIR: DOWN")

    def move_left(self, event):
        self.direction = DIRECTIONS[3]
        print ("DIR: LEFT")

    def draw (self):
        """ Moves the snake depending on the direction, tests borders, draws"""
        for i in range(0, self.length):
            if i == 0 and self.length >= 1:
                self.body[i].draw(self.position)
            elif i > 0 and self.length >= 1:
                self.body[i].draw(self.body[i-1].last_position)

        self.canvas.move(self.id, self.delta_x, self.delta_y)


        self.position = self.canvas.coords(self.id)

        if self.position[0] < 0:
            self.canvas.move(self.id, WIN_WIDTH, 0)
        elif self.position[0] > WIN_WIDTH:
            self.canvas.move(self.id, -WIN_WIDTH,0)
        elif self.position[3] > WIN_HEIGHT:
            self.canvas.move(self.id, 0, -WIN_HEIGHT)
        elif self.position[3] < 0:
            self.canvas.move(self.id, 0, WIN_HEIGHT)

        self.delta_x = 0
        self.delta_y = 0


        if self.direction == DIRECTIONS[0]:
            self.delta_y = - self.speed
        elif self.direction == DIRECTIONS[1]:
            self.delta_x =  self.speed
        elif self.direction == DIRECTIONS[2]:
            self.delta_y = self.speed
        elif self.direction == DIRECTIONS[3]:
            self.delta_x = - self.speed

    position = None
    delta_x = 0
    delta_y = 0
    inside_window = None
    direction = DIRECTIONS[2]
    speed = 2
    length = 0
    body = list()

tk = Tk()
tk.title('Game')
canvas = Canvas(tk, width = WIN_WIDTH, height = WIN_HEIGHT, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

snake = Head (canvas)
falling_fruit = list()

for i in range (0, 200):
    falling_fruit.append(Falling_Fruit (canvas))

while 1:
    if snake.inside_window == True:
        snake.draw()
        for i in range (0, 200):
            falling_fruit[i].draw()
            falling_fruit[i].collision_check(snake)


    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
