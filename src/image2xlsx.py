import os
import time

from tkinter import *
import tkinter.ttk as ttk
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
    save_right_answers()
    path = askdirectory()
    if not path: return
    start_time = time.time()
    all_files = len(list(os.scandir(path)))
    dir_data = os.scandir(path)
    pb['length'] = all_files*3
    n = 0
    for item in dir_data:
        if item.is_file:
            filepath = item.path.replace('/', os.path.sep)
            result = handling.handle(filepath)
            balls[result[0]] = (len(right_answers.intersection(result[1])), [i[0]+' '+i[1] for i in result[1]].sort())
        pb.step(100/all_files)
        pb.update()
        message_string['text'] = f'Обработка... {round(n*100/all_files, 4)}%'
        n += 1
    message_string['text'] = f'Обработано! {round(time.time()-start_time, 4)} c'

def save_file(*args):
    global results_file
    results_file = openpyxl.Workbook()
    results_file.create_sheet(title='New worksheet')
    path = asksaveasfilename(filetypes=[("Excel files", ".xlsx .xls")])
    if not path: return
    results_file.save(path)

def save_right_answers(*args):
    global right_answers
    right_answers = set()
    try:
        for i in right_answers_input.get(0.0, END).split('\n'):
            if i.strip():
                if len(i.strip()) < 2: raise ValueError('') #проверка на правильность синтаксиса
                right_answers.add((i.strip()[0], i.strip()[1:]))
        message_string['bg'] = 'green'
        message_string['text'] = 'All ok'
    except Exception:
        message_string['text'] = 'Неправильный синтаксис ответов!'
        message_string['bg'] = 'red'

message_string = Label(root, text='')
message_string.pack(side=TOP)

pb = ttk.Progressbar(root, length=100)
pb.pack(side=TOP)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="open", command=open_folder)
root.bind_all('<Control-o>', open_folder)
file_menu.add_command(label="save as", command=save_file)
root.bind_all('<Control-s>', save_file)
main_menu.add_cascade(label='File', menu=file_menu)

right_answers_input = Text(root, width=20, height=15)
right_answers_input.pack(side=TOP, padx=60, pady=50)
right_answers_input.bind('<Return>', save_right_answers)

root.mainloop()
