# PetriPro
Welcome to Petris wonderful PetriNet simulator!

## Introduction
PetriPro is a user-friendly tool designed for creating, displaying, and interacting with PetriNets. These PetriNets are generated from datasets read from disk. Currently, we support both _.xes_ (including compressed) and _.csv_ file formats.

## Getting Started
1. **Select a File**: Click on "Browse File" to open a file explorer and select a file in the supported formats.
2. **File Format**: For CSV files, both comma and semicolon delimiters are supported and automatically detected upon reading. We support UTC datetime formats only.
3. **Map Columns**: After file selection, an additional window will prompt you to select the Timestamp, Activity, and Case columns for proper mapping.

## Interacting with Your PetriNet
Once you click "submit", your PetriNet will be displayed. Here's what you need to know about the interface:
- **Initial and Final Places** are marked in grey.
- **Active Transitions** are outlined in red, and selected (or prioritized) ones are filled in bright yellow.
- All other elements are colored in black and white.

You can interact with your model in the following ways:
- **Step Through the Model**: Click the "Step" button to play through the model at random.
- **Prioritize Active Transitions**: Right-click on an active transition to prioritize it.
- **Replay a Trace**: Select a case-id from the list to automatically select and prioritize the corresponding trace.

## Additional Features
- **Rearrange Elements**: Use drag & drop to rearrange the transitions and places as needed.
- **Reset the PetriNet**: Press the reset button to return the PetriNet to its original state.
