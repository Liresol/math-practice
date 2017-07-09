from tkinter import *
from tkinter import ttk
from tkinter import messagebox
session = False
from problem import Problem
import random
import copy
import basicmath
import time
from settings import SettingsWindow
import configparser
import os.path
import stats
config = configparser.ConfigParser()
config.read('config.ini')

#Runs on Python 3.6.1
#TODO: Problem generation, Putting those problems in a Session, Follow style guides, Settings, Question types, Enabling Questions


root = Tk()

class SessionButton:
    def __init__(self, master):
        self.inSession = False
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.button1 = ttk.Button(self.frame, text = 'Start', width = 25, command = self.create_session)
        self.button1.grid()
        self.frame.grid()
    def update_button(self):
        if self.inSession:
            self.button1.destroy()
            self.button1 = ttk.Button(self.frame, text = 'End', width = 25, command = self.end_session)
        else:
            self.button1.destroy()
            self.button1 = ttk.Button(self.frame, text = 'Start', width = 25, command = self.create_session)
        self.button1.grid(row = 0, column = 0)
    def create_session(self):
        if not self.inSession:
            self.session = Session(self.master)
            self.inSession = True
            self.update_button()
            #self.session.set_problem(Problem("3","4"))
            self.session.display_problem()
    def end_session(self):
        if self.inSession:
            self.inSession = False
            self.session.end()
            self.update_button()

class Session:
    def __init__(self, master):
        self.master = master
        #self.frame = Frame(self.master)
        self.frame = ttk.Frame(self.master)
        #Performs shallow copy of the old title
        self.old_title = self.master.title
        self.master.title('Session')
        self.frame['padding'] = (5,10)
        self.frame.grid(column=0,row=1, sticky=(N, E, S, W))
        self.reply = StringVar()
        self.answer = ttk.Entry(self.frame, textvariable = self.reply)
        self.answer.grid(column = 0, row = 2, sticky = (E,W))
        self.master.bind('<Return>', self.evaluate_answer)
        self.new_problem()
        self.ans_num = 0
        self.correct_num = 0
        self.total_time = 0.0
        self.correct_time = 0.0
        self.stats = stats.Stats()
    #May be useful
        basicmath.update_config()
    def set_problem(self, problem):
        self.problem = problem
    def display_problem(self):
        self.label1 = ttk.Label(self.frame, text=self.problem.question, anchor = CENTER, justify=CENTER)
        self.label1.grid(column=0,row=0, sticky=(N, E, S, W))
        self.middle_frame = ttk.Frame(self.frame, height=100, width=300)
        self.middle_frame.grid(column=0, row=1, sticky = (N, E, S, W))

    def evaluate_answer(self, *args):
        self.endtime = time.time()
        print(self.endtime-self.start)
        s = self.reply.get()
        try:
            self.problem.evaluate_answer(s)
            #print("the yes")
        except ValueError:
            print("Invalid Answer")
            pass
        if self.problem.correct:
            print("True")
        else:
            print("Untrue")
            print(self.problem.answer)
        self.tally_answers()
        self.answer.delete(0, END)
        self.new_problem()
    def new_problem(self):
        self.set_problem(make_question())
        self.display_problem()
        self.start = time.time()
    def destroy_problem(self):
        self.label1.destroy()
    def tally_answers(self):
        if self.problem.answered:
            self.stats.add_time(self.problem.category, self.endtime - self.start, self.problem.correct)
            self.ans_num += 1
            if self.problem.correct:
                self.correct_num += 1
                self.correct_time += self.endtime - self.start
            self.total_time += self.endtime - self.start
    def print_summary(self):
        print()
        print("Accuracy:")
        print(str(self.correct_num) + " / " + str(self.ans_num))
        if self.ans_num > 0:
            print("Average time:")
            print(str(self.total_time / self.ans_num) + "s")
        else:
            print("No questions answered")
        if self.correct_num > 0:
            print("Average time for correct answers:")
            print(str(self.correct_time / self.correct_num) + "s")
        elif self.ans_num > 0:
            print("No correct answers")
    def end(self):
        self.print_summary()
        self.destroy_problem()
        self.frame.destroy()
        stats.StatsWriter.write_session(self.stats)
        self.master.title = self.old_title

#Creates a random problem
"""
Creates a random problem from the list
"""
def make_question():
    list = [basicmath.addition_problem, basicmath.subtraction_problem, basicmath.multiplication_problem, basicmath.integer_division_problem]

    return list[random.randint(0,len(list)-1)]()

def make_default_config():
    config['Addition'] = {'min': 10, 'max': 100}
    config['Subtraction'] = {'min': 10, 'max': 100}
    config['Multiplication'] = {'min': 10, 'max': 50}
    config['Division'] = {'min': 10, 'max': 50}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

#TODO: RENAME
"""
Opens the settings window
"""
def open_settings():
    settings = SettingsWindow(root)
def open_stats():
    s = stats.StatsWindow(root)
def delete_stats():
    if messagebox.askokcancel("Delete", "Delete all stats?"):
        stats.StatsWriter.delete_stats()

def main():
    root.option_add('*tearOff', FALSE)
    #root.title("Test thing")
    #win = Toplevel(root)
    root.title("Math Stuff")
    mainfram = ttk.Frame(root, padding="4 12")
    menubar = Menu(root)
    menu_settings = Menu(menubar)
    menu_stats = Menu(menubar)
    menubar.add_cascade(menu=menu_settings, label='Settings')
    menubar.add_cascade(menu=menu_stats, label='Stats')
    root.resizable(False,False)
    button = SessionButton(root)
    #test = Session(root)
    #Lel
    menu_settings.add_command(label='Do Thing', command=open_settings)
    menu_stats.add_command(label='Open Stats', command=open_stats)
    menu_stats.add_command(label='Delete Stats', command=delete_stats)
    root['menu'] = menubar
    root.mainloop()
    #settings = SettingsWindow(root)


if __name__ == "__main__":
    if not os.path.isfile('config.ini'):
        make_default_config()
    main()
