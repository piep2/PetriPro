import tkinter as tk
import math
import re
import random as rng

class Node:
    def __init__(self, canvas, x, y, text, shape):
        self.selected = False
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.shape = shape
        self.text_id = self.canvas.create_text(self.x, self.y, text=self.text, fill="black")
        self.bbox = self.canvas.bbox(self.text_id)
        if self.shape == "circle":
            self.r = 25
            self.id = self.canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill='white')
        elif self.shape == "rectangle":
            w = (self.bbox[2] - self.bbox[0])
            h = (self.bbox[3] - self.bbox[1])
            self.left = (self.x - w/2 - 10, self.y)
            self.top = (self.x, self.y + h/2 + 10)
            self.right = (self.x + w/2 + 10, self.y)
            self.bottom = (self.x, self.y - h/2 - 10)
            self.id = self.canvas.create_rectangle(self.bbox[0]-10, self.bbox[1]-10, self.bbox[2]+10, self.bbox[3]+10, fill='white')
            
        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_bind(self.id, '<Button-3>', self.click)
        self.canvas.tag_bind(self.text_id, '<Button-3>', self.click)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.move)
        self.canvas.tag_bind(self.text_id, '<B1-Motion>', self.move)

    def move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)
        self.x = event.x
        self.y = event.y

        w = (self.bbox[2] - self.bbox[0])
        h = (self.bbox[3] - self.bbox[1])
        self.left = (self.x - w/2 - 10, self.y)
        self.top = (self.x, self.y + h/2 + 10)
        self.right = (self.x + w/2 + 10, self.y)
        self.bottom = (self.x, self.y - h/2 - 10)
        self.canvas.update()
        

    def click(self, event):
        if self.selected:
            self.canvas.itemconfig(self.id, outline="black")
            self.selected=False
        else:
            self.canvas.itemconfig(self.id, outline="blue")
            self.selected=True


class Arrow:
    def __init__(self, canvas, node1, node2):
        self.canvas = canvas
        self.node1 = node1
        self.node2 = node2
        self.id = self.canvas.create_line(self.node1.x, self.node1.y, self.node2.x, self.node2.y, arrow=tk.LAST)

    def update(self):
        dx = self.node2.x - self.node1.x
        dy = self.node2.y - self.node1.y
        angle = math.atan2(dy, dx)
        if self.node1.shape == "circle":
            x1 = self.node1.x + self.node1.r * math.cos(angle)
            y1 = self.node1.y + self.node1.r * math.sin(angle)
        else:
            left = dx <= 0
            top = dy >= 0
            side = abs(dx) >= abs(dy)
            if side and left:
                x1 = self.node1.left[0]
                y1 = self.node1.left[1]
            elif side and not left:
                x1 = self.node1.right[0]
                y1 = self.node1.right[1]
            elif not side and top:
                x1 = self.node1.top[0]
                y1 = self.node1.top[1]
            elif not side and not top:
                x1 = self.node1.bottom[0]
                y1 = self.node1.bottom[1]


        if self.node2.shape == "circle":
            x2 = self.node2.x - self.node2.r * math.cos(angle)
            y2 = self.node2.y - self.node2.r * math.sin(angle)
        else:
            left = dx <= 0
            left = not left
            top = dy >= 0
            top = not top
            side = abs(dx) >= abs(dy)

            if side and left:
                x2 = self.node2.left[0]
                y2 = self.node2.left[1]
            elif side and not left:
                x2 = self.node2.right[0]
                y2 = self.node2.right[1]
            elif not side and top:
                x2 = self.node2.top[0]
                y2 = self.node2.top[1]
            elif not side and not top:
                x2 = self.node2.bottom[0]
                y2 = self.node2.bottom[1]

        self.canvas.coords(self.id, x1, y1, x2, y2)

class App:
    def __init__(self, places, transitions, arcs):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack()

        self.places = places
        for place in self.places:
            self.places[place]["gui_object"] = Node(self.canvas, rng.randint(100, 800), rng.randint(100, 800), str(self.places[place]["tokens"]) if self.places[place]["tokens"] > 0 else "", "circle")
        
        self.transitions = transitions
        for trans in self.transitions:
            self.transitions[trans]["gui_object"] = Node(self.canvas, rng.randint(100, 800), rng.randint(100, 800), trans, "rectangle")

        self.arcs = []
        for arc in arcs:
            src = self.transitions[arc["source"]]["gui_object"] if arc["source"] in self.transitions.keys() else self.places[arc["source"]]["gui_object"]
            dst = self.transitions[arc["dest"]]["gui_object"] if arc["dest"] in self.transitions.keys() else self.places[arc["dest"]]["gui_object"]

            self.arcs.append(Arrow(self.canvas, src, dst))

        self.root.after(100, self.update)
        self.root.mainloop()

    def update(self):
        for arc in self.arcs:
            arc.update()
        self.root.after(100, self.update)






