import paho.mqtt.client as paho
import tkinter as tkin
import time
import random
from visualisation import visualisation_heatmap

broker="172.19.0.3"
port=1883
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


def good_func():
    print("do something good")
    pass

client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                                 #establish connection

tk = tkin.Tk()
tk.title('Game')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
height = 600
canvas = tkin.Canvas(tk, width=800, height=height, highlightthickness=0)
canvas.pack()
tk.update()


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 30, 30, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-2, -1, 1, 2]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -2
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 2
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 120, text='Вы проиграли', font=('Courier', 30), fill='red')
        if self.hit_paddle(pos) == True:
            self.y = -5
        if pos[0] <= 0:
            self.x = 2
        if pos[2] >= self.canvas_width:
            self.x = -2
        return(pos)


class Paddle:
    def __init__(self, canvas, color, height = height):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(start_1)
        self.starting_point_x = start_1[0]
        self.canvas.move(self.id, self.starting_point_x, height-100)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.started = False
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)
    def turn_right(self, event):
        self.x = 5
    def turn_left(self, event):
        self.x = -5
    def start_game(self, event):
        self.started = True
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0
        return (pos)

try:
    paddle = Paddle(canvas, 'White', height)
    ball = Ball(canvas, paddle, 'red')
    while not ball.hit_bottom:
        if paddle.started == True:
            ball_position = ball.draw()
            paddle_position = paddle.draw()
            ball_data = "coordinates,object=ball x_coord={0},y_coord={1}".format(ball_position[0] + 10, ball_position[1] + 10)
            paddle_data = "coordinates,object=paddle x_coord={0},y_coord={1}".format(paddle_position[0], 100)
            client1.publish("arkanoid", ball_data)
            client1.publish("arkanoid", paddle_data)
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
    client1.disconnect()
except KeyboardInterrupt:
    client1.disconnect()

time.sleep(3)
visualisation_heatmap()
