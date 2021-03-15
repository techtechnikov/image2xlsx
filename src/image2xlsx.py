import os

from tkinter import *
from tkinter.filedialog import askdirectory, asksaveasfilename

import handling

import openpyxl

path = ''

root = Tk()
main_menu = Menu(root)
root.config(menu=main_menu)

def open_folder(*args):
    path = askdirectory()
    for item in os.scandir(path):
        if item.is_file:
            filepath = item.path.replace('/', os.path.sep)
            handling.handle(filepath)

def save_file(*args):
    pass
    

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="open", command=open_folder)
root.bind_all('<Control-o>', open_folder)
file_menu.add_command(label="save as")
main_menu.add_cascade(label='File', menu=file_menu)

right_answers_input = Text(root, width=20, height=15)
right_answers_input.pack()
root.mainloop()
