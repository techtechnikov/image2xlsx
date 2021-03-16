import os

from tkinter import *
from tkinter.filedialog import askdirectory, asksaveasfilename

import handling

import openpyxl

path = ''
balls = {}
right_answers = set()

root = Tk()
main_menu = Menu(root)
root.config(menu=main_menu)

def open_folder(*args):
    global balls
    path = askdirectory()
    if not path: return
    for item in os.scandir(path):
        if item.is_file:
            filepath = item.path.replace('/', os.path.sep)
            result = handling.handle(filepath)
            balls[result[0]] = (len(right_answers.intersection(result[1])), [i[0]+' '+i[1] for i in result[1]].sort())

def save_file(*args):
    pass

def save_right_answers(*args):
    global right_answers
    try:
        right_answers = {(i.strip()[0], i.strip()[1:]) for i in right_answers_input.get(0.0, END).split('\n')[:-1]}
        message_string['bg'] = 'green'
        message_string['text'] = 'All ok'
    except Exception:
        message_string['text'] = 'Неправильный синтаксис ответов!'
        message_string['bg'] = 'red'

message_string = Label(root, text='')
message_string.pack(side=TOP)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="open", command=open_folder)
root.bind_all('<Control-o>', open_folder)
file_menu.add_command(label="save as")
main_menu.add_cascade(label='File', menu=file_menu)

right_answers_input = Text(root, width=20, height=15)
right_answers_input.pack(side=TOP, padx=60, pady=50)
right_answers_input.bind('<Return>', save_right_answers)

root.mainloop()
