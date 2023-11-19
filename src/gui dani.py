import tkinter as tk

# Function to handle button click
def on_button_click(transition_name):
    print(f"{transition_name} clicked")

# Function to handle object movement
def on_object_move(event, obj, text=None):
    # Get the current position of the object
    x, y, _, _ = canvas.coords(obj)
    # Calculate the new position of the object
    dx = event.x - x
    dy = event.y - y
    # Move the object
    canvas.move(obj, dx, dy)
    # Move the text if it exists
    if text:
        canvas.move(text, dx, dy)
    # Redraw the arrows
    for arrow in arrows:
        canvas.delete(arrow)
    arrows.clear()
    draw_arrows()

def draw_arrows():
    for arc in arcs:
        source = arc['source']
        target = arc['target']
        if source in transitions:
            x1, y1, _, _ = canvas.coords(transitions[source][0])
        else:
            x1, y1, _, _ = canvas.coords(places[source])
        if target in transitions:
            x2, y2, _, _ = canvas.coords(transitions[target][0])
        else:
            x2, y2, _, _ = canvas.coords(places[target])
        arrow = canvas.create_line(x1+25, y1+50, x2+25, y2+25, arrow=tk.LAST)
        arrows.append(arrow)

# Create the main window
root = tk.Tk()

# Create a canvas to draw on
canvas = tk.Canvas(root, width=2000, height=2000)
canvas.pack()

# List of transitions and places
transitions = {}
places = {}

# List to store the arrows
arrows = []

# Define the transitions, places, and arcs
transitions = {"(Transition 1, 'Transition 1')": (100, 200),
               "(Transition 2, 'Transition 2')": (200, 300),
               "(Transition 3, 'Transition 3')": (300, 200)}

places = {'start': (50, 200),
          'end': (350, 200),
          "({'Transition 1'}, {'Transition 2'})": (150, 100),
          "({'Transition 2'}, {'Transition 3'})": (250, 100),
          "({'Transition 3'}, {'Transition 2'})": (250, 300)}

arcs = [
    {'source': 'start', 'target': "(Transition 1, 'Transition 1')"},
    {'source': "(Transition 1, 'Transition 1')",
     'target': "({'Transition 1'}, {'Transition 2'})"},
    {'source': "({'Transition 1'}, {'Transition 2'})",
     'target': "(Transition 2, 'Transition 2')"},
    {'source': "(Transition 2, 'Transition 2')",
     'target': "({'Transition 2'}, {'Transition 3'})"},
    {'source': "({'Transition 2'}, {'Transition 3'})",
     'target': "(Transition 3, 'Transition 3')"},
    {'source': "(Transition 3, 'Transition 3')",
     'target': "({'Transition 3'}, {'Transition 2'})"},
    {'source': "({'Transition 3'}, {'Transition 2'})",
     'target': "(Transition 2, 'Transition 2')"},
    {'source': "(Transition 3, 'Transition 3')",
     'target': "end"}
]

for name, (x, y) in transitions.items():
    # Draw a rectangle for the transition
    transition = canvas.create_rectangle(x, y, x+50, y+100, fill='light blue')
    # Add text to the rectangle
    text = canvas.create_text(x+25, y+50, text=name)
    transitions[name] = (transition, text)
    # Bind the click event to the rectangle
    canvas.tag_bind(transition, '<Button-1>', lambda event, t=name: on_button_click(t))
    # Bind the movement event to the rectangle
    canvas.tag_bind(transition, '<B1-Motion>', lambda event, obj=transition, txt=text: on_object_move(event, obj, txt))

for name, (x, y) in places.items():
    # Draw a circle for the place
    place = canvas.create_oval(x, y, x+50, y+50, fill='red')
    places[name] = place
    # Bind the movement event to the circle
    canvas.tag_bind(place, '<B1-Motion>', lambda event, obj=place: on_object_move(event, obj))

# Draw arrows between the places and transitions
draw_arrows()

# Start the main loop
root.mainloop()
