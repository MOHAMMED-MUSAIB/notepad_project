import tkinter as tk
import os
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Notepad:
    
    __root = Tk()
    
    # Default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    
    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)     
    __file = None

    def __init__(self, **kwargs):
        
        # Set icon (optional)
        try:
            self.__root.wm_iconbitmap("Notepad.ico") 
        except:
            pass

        # Set window size (default is 300x300)
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window title
        self.__root.title("Untitled - Notepad")

        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left-align
        left = (screenWidth / 2) - (self.__thisWidth / 2) 

        # For top-align
        top = (screenHeight / 2) - (self.__thisHeight / 2) 

        # Set window geometry
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        # To make the textarea auto-resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky=N+E+S+W)
        
        # File menu options
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        # Edit menu options
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        # Help menu option
        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        # Configure the menu
        self.__root.config(menu=self.__thisMenuBar)

        # Scrollbar setup
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    # Quit the application
    def __quitApplication(self):
        self.__root.destroy()

    # Show the 'About' message box
    def __showAbout(self):
        showinfo("Notepad", "Simple Notepad application made with Tkinter")

    # Open a file
    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files", "*.*"), 
                                                 ("Text Documents", "*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            # Try to open the file and set the window title
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)
            with open(self.__file, "r") as file:
                self.__thisTextArea.insert(1.0, file.read())

    # Create a new file
    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    # Save the current file
    def __saveFile(self):
        if self.__file is None:
            # Save as a new file
            self.__file = asksaveasfilename(initialfile="Untitled.txt",
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.txt")])
            if self.__file == "":
                self.__file = None
            else:
                # Try to save the file
                with open(self.__file, "w") as file:
                    file.write(self.__thisTextArea.get(1.0, END))
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
        else:
            # Save the current file
            with open(self.__file, "w") as file:
                file.write(self.__thisTextArea.get(1.0, END))

    # Cut the selected text
    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    # Copy the selected text
    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    # Paste the copied text
    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    # Run the Notepad application
    def run(self):
        self.__root.mainloop()

# Run the main application
notepad = Notepad(width=600, height=400)
notepad.run()
