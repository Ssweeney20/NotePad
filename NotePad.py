import tkinter
import time


# Store Memory (Memento Objects)
class History:
    # List for storing savestates
    obj = []

    # List for storing undone save states
    objR = []

    # Saves a memento object with the current text to the savestate list

    def save(self, text):
        self.obj.append(saveT())

    # Takes most recent save state(other then the current), pops and removes it from the list. Adds this to the redo savestate list. Calls the main undo function on this savestate

    def undo(self, text):
        n = len(self.obj) - 1
        self.objR.append(saveT())
        undoT(self.obj[n-1])
        del(self.obj[n-1])

    # Takes the most recent save state from the redo state list, and calls the undo function for it. It removes this from the Rlist, and adds this to the undo state list.

    def redo(self, text):
        n = len(self.objR)
        self.obj.append(saveT())
        undoT(self.objR[n-1])
        del(self.objR[n-1])


# Memory Objects
class Memento:

    def __init__(self, content):
        self.content = content


# Returns an object containing the contents of the textbox
def saveT():
    return Memento(text.get(0.0, "end"))


# Replaces the current text on the screen with the content of a memento object
def undoT(memento):
    # reinsert text to text box here.
    replacement_text = memento.content
    text.delete(0.0, "end")
    text.insert(0.0, replacement_text)


# Function for command line saving.
def save():
    # Variable for all text on the screen.
    saved_text = text.get(0.0, "end")
    # Asks for the name of the file.
    try:
        file_name = input("What would you like to name this file?\n")
        # Opens File, if exception is thrown that the file doesn't exist, we create a new file (except)
        try:
            document = open(file_name + '.txt', 'r')
        except:
            document = open(file_name + '.txt', 'x')
            document.write(saved_text)
            document.close()
        else:
            # Overwrite check
            if document.name == file_name + ".txt":
                user_inp = input(
                    "This document already exists, would you like to overwrite? (Yes/No)\n")
                if user_inp.lower() == "yes":
                    document = open(file_name + '.txt', 'w')
                    document.write(saved_text)
                    document.close()
                    print("File has been overwritten")
                elif user_inp.lower() == "no":
                    print("Not overwriting")
                    document.close()
                else:
                    print("incorrect input")
    except:
        pass


# Function to load a file
def load():
    # Asks for the name of the file.
    try:
        file_name = input("Which file would you like to load?\n")
        # Attempts to open the file by the specified name. Then the text of the current file is deleted and replaced with the content of the loaded file.
        try:
            f = open(file_name + '.txt', 'r')
            replacement_text = f.read()
            text.delete(0.0, "end")
            text.insert(0.0, replacement_text)
            f.close()
            print("The file has been loaded.")

        # Runs if the file does not exist.
        except:
            print("No file by the name " + file_name + " exists")
    except:
        pass


# Loads past save state
def undo():
    H.undo(text)


# Loads the save state of a recently undone text
def redo():
    H.redo(text)


# Creates a save state with the text onscreen
def saveState(History):
    H.save(text)


# Creates object to store savestates
H = History()

# Creates Window
WIN = tkinter.Tk()
text = tkinter.Text(height=30, width=120)
text.pack()

# Buttons
btnRead = tkinter.Button(height=1, width=10, text="Save",
                         command=save)
btnRead2 = tkinter.Button(height=1, width=10, text="Load",
                          command=load)
btnRead3 = tkinter.Button(height=1, width=10, text="Redo",
                          command=redo)
btnRead4 = tkinter.Button(height=1, width=10, text="Undo",
                          command=undo)
btnRead.pack()
btnRead2.pack()
btnRead3.pack()
btnRead4.pack()

# Creates and stores inital save state for undo purposes
H.save(text)

# Whenever a key is pressed a new save state is created and stored with the new text. This is for undo purposes.
WIN.bind("<Key>", saveState)

WIN.mainloop()
