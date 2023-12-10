import tkinter as tk
import math
import re
import random as rng
import pm4py
import pandas as pd
from tkinter import filedialog
import ttkbootstrap as ttk
import ttkbootstrap.constants as bt_constants
import numpy as np

class Node:
    def __init__(self, canvas, x, y, text, nodeName, shape):
        self.selected = False
        self.active = False
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.shape = shape
        self.text_id = self.canvas.create_text(self.x, self.y, text=self.text, fill="black")
        self.bbox = self.canvas.bbox(self.text_id)

        fill_color = "white" if nodeName not in ["start", "end"] else "#D7D7D7"

        if self.shape == "circle":
            self.r = 25
            self.id = self.canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=fill_color)
        elif self.shape == "rectangle":
            w = (self.bbox[2] - self.bbox[0])
            h = (self.bbox[3] - self.bbox[1])
            self.left = (self.x - w/2 - 10, self.y)
            self.top = (self.x, self.y + h/2 + 10)
            self.right = (self.x + w/2 + 10, self.y)
            self.bottom = (self.x, self.y - h/2 - 10)
            self.id = self.canvas.create_rectangle(self.bbox[0]-10, self.bbox[1]-10, self.bbox[2]+10, self.bbox[3]+10, fill=fill_color)
            
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
        if self.selected and self.active:
            self.canvas.itemconfig(self.id, outline="red")
            self.selected=False
        elif self.selected:
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
    def isActive(self, trans):
        active = len(trans.in_arcs) > 0
        counter = 0

        # check all places of incoming arcs whether they satisfy the token count (arc weight)
        while active and counter < len(trans.in_arcs):
            placeName = str(list(trans.in_arcs)[counter]).split("->")[0]
            if self.places[placeName]["gui_object"] is not None and self.places[placeName]["tokens"] < list(trans.in_arcs)[counter].weight:
                active = False
            counter += 1

        return active

    def step(self):
        actives = []

        # First, iterate through all transitions and determine all that COULD be fired
        for trans in self.transitions:
            if self.transitions[trans]["gui_object"] is not None:
                if self.isActive(self.transitions[trans]["pm4py_object"]):
                    actives.append(self.transitions[trans]["pm4py_object"])

        # fire as many transitions as possible
        while len(actives) > 0:
            # choose a random transition
            prioritized = [trans for trans in actives if self.transitions[str(trans)]["gui_object"] is not None and self.transitions[str(trans)]["gui_object"].selected]

            if prioritized:
                chosenTrans = rng.choice(prioritized)
            else:
                chosenTrans = rng.choice(actives)
            actives.remove(chosenTrans)

            # Then, iterate through all connected places and consume their tokens
            for inArc in chosenTrans.in_arcs:
                placeName = str(inArc).split("->")[0]
                if self.places[placeName]["gui_object"] is not None:
                    self.places[placeName]["tokens"] -= inArc.weight
                    self.canvas.itemconfig( self.places[placeName]["gui_object"].text_id, 
                                            text=str(self.places[placeName]["tokens"]) if self.places[placeName]["tokens"] > 0 else "")

                    # After consuming the tokens, the remaining transitions connected to this place need to be reevaluated (if they are still active, since the token count has changed)
                    for outArc in self.places[placeName]["pm4py_object"].out_arcs:
                        transName = str(outArc).split("->")[1]
                        otherTrans = self.transitions[transName]["pm4py_object"]
                        if transName != str(chosenTrans) and chosenTrans in self.transitions and not self.isActive(otherTrans) and otherTrans in actives:
                            actives.remove(otherTrans)

            # Finally, new tokens are created for all outgoing places connected to the firing transition
            for outArc in chosenTrans.out_arcs:
                placeName = str(outArc).split("->")[1]
                if self.places[placeName]["gui_object"] is not None:
                    self.places[placeName]["tokens"] += outArc.weight
                    self.canvas.itemconfig( self.places[placeName]["gui_object"].text_id, 
                                            text=str(self.places[placeName]["tokens"]) if self.places[placeName]["tokens"] > 0 else "")

        # color the new actives and refresh the canvas with token counts
        self.colorActives()
        self.canvas.update()

    def colorActives(self):
        actives = []
        
        for trans in self.transitions:
            if self.placementAlreadyCalculated(trans):
                self.transitions[trans]["gui_object"].selected = False
                active = self.isActive(self.transitions[trans]["pm4py_object"])

                if active:
                    actives.append(self.transitions[trans]["pm4py_object"])
                    self.transitions[trans]["gui_object"].active = True
                    self.canvas.itemconfig(self.transitions[trans]["gui_object"].id, outline="red")
                else:
                    self.transitions[trans]["gui_object"].active = False
                    self.canvas.itemconfig(self.transitions[trans]["gui_object"].id, outline="black")


        self.canvas.update()

            
    def getPlacements(self, currentNode, col):
        if col not in self.placements.keys():
            self.placements[col] = []

        self.placements[col].append(str(currentNode))
        for outArc in currentNode.out_arcs:
            outName = str(outArc).split("->")[1]
            if outName in self.transitions.keys():
                outNode = self.transitions[outName]["pm4py_object"]
            else:
                outNode = self.places[outName]["pm4py_object"]

            if not self.placementAlreadyCalculated(outName):
                self.getPlacements(outNode, col+1)

        for outArc in currentNode.in_arcs:
            outName = str(outArc).split("->")[0]
            if outName in self.transitions.keys():
                outNode = self.transitions[outName]["pm4py_object"]
            else:
                outNode = self.places[outName]["pm4py_object"]

            if not self.placementAlreadyCalculated(outName):
                self.getPlacements(outNode, max(col-1, 0))


    def correctTransitionPlacement(self):
        for trans in self.transitions:
            if self.placementAlreadyCalculated(trans):
                x, _ = self.getPlacement(trans)
                #newX = (np.average([self.getPlacement(str(arc).split("->")[0])[0] for arc in self.transitions[trans]["pm4py_object"].in_arcs]) + 
                #np.average([self.getPlacement(str(arc).split("->")[1])[0] for arc in self.transitions[trans]["pm4py_object"].out_arcs])) / 2
                newX = np.min([self.getPlacement(str(arc).split("->")[0])[0] for arc in [x for x in self.transitions[trans]["pm4py_object"].in_arcs if self.placementAlreadyCalculated(str(x).split("->")[0])]] + [self.getPlacement(str(arc).split("->")[1])[0] for arc in [x for x in self.transitions[trans]["pm4py_object"].out_arcs if self.placementAlreadyCalculated(str(x).split("->")[1])]]) + 1
                
                self.placements[x].remove(trans)
                if int(newX) not in self.placements.keys():
                    self.placements[int(newX)] = []
                self.placements[int(newX)].append(trans)

    def getPlacement(self, nodeName):
        col = 0
        while nodeName not in self.placements[col]:
            col += 1

        return col, self.placements[col].index(nodeName)
    
    def placementAlreadyCalculated(self, nodeName):
        col = 0
        while col in self.placements.keys() and nodeName not in self.placements[col]:
            col += 1

        return col in self.placements.keys()
                
        
    def draw_components(self):
        badPlaces = []
        for place in self.places:
            if self.placementAlreadyCalculated(place):
                x, y = self.getPlacement(place)
                self.places[place]["gui_object"] = Node(self.canvas, x * self.distanceFactorX + self.offsetX, y * self.distanceFactorY + self.offsetY, str(self.places[place]["tokens"]) if self.places[place]["tokens"] > 0 else "", place, "circle")
            else:
                badPlaces.append(place)

        badTransitions = []
        for trans in self.transitions:
            if self.placementAlreadyCalculated(trans):
                x, y = self.getPlacement(trans)
                self.transitions[trans]["gui_object"] = Node(self.canvas, x * self.distanceFactorX + self.offsetX, y * self.distanceFactorY + self.offsetY, trans.split("'")[1], trans, "rectangle")
            else:
                badTransitions.append(trans)

        self.arcs = []
        for arc in self.arcDict:
            src = self.transitions[arc["source"]]["gui_object"] if arc["source"] in self.transitions.keys() else self.places[arc["source"]]["gui_object"]
            dst = self.transitions[arc["dest"]]["gui_object"] if arc["dest"] in self.transitions.keys() else self.places[arc["dest"]]["gui_object"]

            if src is not None and dst is not None:
                self.arcs.append(Arrow(self.canvas, src, dst))
    
        self.colorActives()
        self.getPlacements(self.places["start"]["pm4py_object"], 0)
        self.correctTransitionPlacement()
                

    def browseFiles(self):
        self.filePath = filedialog.askopenfilename(initialdir = ".",
                                          title = "Select a File",
                                          filetypes = (("CSV files",
                                                        "*.csv*"),
                                                       ("XES files",
                                                        "*.xes*")))
        self.redrawPetriNet()
        

    def redrawPetriNet(self):
        self.canvas.delete('all')
        self.compute_gui_components(self.filePath)
        self.draw_components()


    def __init__(self):
        self.placements = dict()
        self.offsetX = 100
        self.offsetY = 100
        self.distanceFactorX = 130
        self.distanceFactorY = 100
        
        self.places = []
        self.transitions = []
        self.arcs = []
        
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack()

        self.play_button = ttk.Button(self.root, text="Step", width=5, command=self.step, bootstyle=bt_constants.SUCCESS)
        self.play_button.place(x=10, y=10)


        self.button_explore = ttk.Button(self.root, text = "Browse Files", width=10, command = self.browseFiles, bootstyle=bt_constants.PRIMARY) 
        self.button_explore.place(x=10, y=55)

        self.button_reset = ttk.Button(self.root, text = "Reset", width=10, command = self.redrawPetriNet, bootstyle=bt_constants.DANGER) 
        self.button_reset.place(x=10, y=100)

        self.root.after(100, self.update)
        self.root.mainloop()

    def update(self):
        for arc in self.arcs:
            arc.update()
        self.root.after(100, self.update)


    def compute_gui_components(self, path = "data/running-example.csv"):
        dataframe = pd.read_csv(path, sep=';')
        dataframe["Timestamp"] = pd.to_datetime(dataframe["Timestamp"], format="%d-%m-%Y:%H.%M")
        dataframe = pm4py.format_dataframe(dataframe, case_id='Case ID', activity_key='Activity', timestamp_key='Timestamp')
        petri, im, fm = pm4py.discover_petri_net_alpha(dataframe)

        placesDict = dict()
        for place in petri.places:
            placesDict[str(place)] = {
                "pm4py_object": place,
                "gui_object": None,
                "tokens": dict(im)[place] if place in dict(im).keys() else 0
            }


        transDict = dict()
        for trans in petri.transitions:
            transDict[str(trans)] = {
                "pm4py_object": trans,
                "gui_object": None,
            }

        arcs = [{"source": str(x).split("->")[0], "dest": str(x).split("->")[1]} for x in petri.arcs]
        self.places = placesDict.copy()
        self.transitions = transDict.copy()
        self.arcDict = arcs.copy()



if __name__ == "__main__":
    app = App()
