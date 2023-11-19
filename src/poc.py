transitions = {"(Transition 1, 'Transition 1')": object,
 "(Transition 2, 'Transition 2')": object,
 "(Transition 3, 'Transition 3')": object}

places = {'start': object,
 'end': object,
 "({'Transition 1'}, {'Transition 2'})": object,
 "({'Transition 2'}, {'Transition 3'})": object,
 "({'Transition 3'}, {'Transition 2'})": object}

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