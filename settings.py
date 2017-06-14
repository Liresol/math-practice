import configparser
from tkinter import *

#Enabling and disabling question types
#Text may not even be necessary
class SettingsWindow:
    def __init__(self, master):
        self.text = ""
        self.dict = {}
        #Magic number
        self.row = 0
        self.config = configparser.ConfigParser()
        self.master = master
        self.read_settings()
        #Starts the dropdown of various settings
        self.window = Toplevel(master, height = 50)
        self.button1 = ttk.Button(self.window, text = 'Save & Quit', command = self.on_closing)
        self.button1.grid(row = 3, column = 1, sticky = (E))
        self.button2 = ttk.Button(self.window, text = 'Cancel & Quit', command = self.cancel_closing)
        self.button2.grid(row = 3, column = 0, sticky = (W))
        self.type = StringVar()
        self.selections = ttk.Combobox(self.window, textvariable = self.type)
        self.selections['values'] = ('Addition', 'Subtraction', 'Multiplication', 'Division')
        self.selections.bind('<<ComboboxSelected>>',self.parse_display)
        self.selections.grid(row = 1, column = 0, columnspan = 2)
        self.frame = ttk.Frame(self.window, height = 100, padding = (5, 10))
        self.frame.grid(row = 2, column = 0, columnspan = 2)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.title("Settings")

    def parse_display(self, *args):
        self.clean_display()
        self.text = self.type.get()
        if self.text == 'Addition':
            self.addition_display()
        elif self.text == 'Subtraction':
            self.subtraction_display()
        elif self.text == 'Multiplication':
            self.multiplication_display()
        elif self.text == 'Division':
            self.int_division_display()
        #Change
        for k, item in self.dict.items():
            item.grid(row = self.row, column = 1, columnspan = 1)
            self.row += 1
        #pass
    def addition_display(self):
        self.entrybox1 = ttk.Entry(self.frame)
        self.entrybox2 = ttk.Entry(self.frame)
        self.label1 = ttk.Label(self.frame, text='Minimum: ')
        self.label2 = ttk.Label(self.frame, text='Maximum: ')
        self.label1.grid(row = 0, column = 0)
        self.label2.grid(row = 1, column = 0)
        if 'Addition' in self.config:
            self.entrybox1.insert(0,self.config['Addition']['min'])
            self.entrybox2.insert(0,self.config['Addition']['max'])
        else:
            self.entrybox1.insert(0,'10')
            self.entrybox2.insert(0,'100')
#        self.entrybox2.insert(0,'100')
        self.dict['min'] = self.entrybox1
        self.dict['max'] = self.entrybox2
        #pass
    def subtraction_display(self):
        self.entrybox1 = ttk.Entry(self.frame)
        self.entrybox2 = ttk.Entry(self.frame)
        self.label1 = ttk.Label(self.frame, text='Minimum: ')
        self.label2 = ttk.Label(self.frame, text='Maximum: ')
        self.label1.grid(row = 0, column = 0)
        self.label2.grid(row = 1, column = 0)
        if 'Subtraction' in self.config:
            self.entrybox1.insert(0,self.config['Subtraction']['min'])
            self.entrybox2.insert(0,self.config['Subtraction']['max'])
        else:
            self.entrybox1.insert(0,'10')
            self.entrybox2.insert(0,'100')
#        self.entrybox2.insert(0,'100')
        self.dict['min'] = self.entrybox1
        self.dict['max'] = self.entrybox2
        #pass
    def multiplication_display(self):
        self.entrybox1 = ttk.Entry(self.frame)
        self.entrybox2 = ttk.Entry(self.frame)
        self.label1 = ttk.Label(self.frame, text='Minimum: ')
        self.label2 = ttk.Label(self.frame, text='Maximum: ')
        self.label1.grid(row = 0, column = 0)
        self.label2.grid(row = 1, column = 0)
        if 'Multiplication' in self.config:
            self.entrybox1.insert(0,self.config['Multiplication']['min'])
            self.entrybox2.insert(0,self.config['Multiplication']['max'])
        else:
            self.entrybox1.insert(0,'10')
            self.entrybox2.insert(0,'100')
#        self.entrybox2.insert(0,'100')
        self.dict['min'] = self.entrybox1
        self.dict['max'] = self.entrybox2
        #pass
    def int_division_display(self):
        self.entrybox1 = ttk.Entry(self.frame)
        self.entrybox2 = ttk.Entry(self.frame)
        self.label1 = ttk.Label(self.frame, text='Minimum: ')
        self.label2 = ttk.Label(self.frame, text='Maximum: ')
        self.label1.grid(row = 0, column = 0)
        self.label2.grid(row = 1, column = 0)
        if 'Division' in self.config:
            self.entrybox1.insert(0,int(self.config['Division']['min']))
            self.entrybox2.insert(0,int(self.config['Division']['max']))
        else:
            self.entrybox1.insert(0,'10')
            self.entrybox2.insert(0,'100')
#        self.entrybox2.insert(0,'100')
        self.dict['min'] = self.entrybox1
        self.dict['max'] = self.entrybox2
        #pass
    def validate_input(self):
        #Checking addition
        if self.text == 'Addition':
            if int(self.dict['min'].get()) > int(self.dict['max'].get()):
                self.dict['min'].delete(0, 'end')
                return False
        #Checking subtraction
        elif self.text == 'Subtraction':
            if int(self.dict['min'].get()) > int(self.dict['max'].get()):
                self.dict['min'].delete(0, 'end')
                return False
        elif self.text == 'Multiplication':
            if int(self.dict['min'].get()) > int(self.dict['max'].get()):
                self.dict['min'].delete(0, 'end')
                return False
        elif self.text == 'Division':
            if int(self.dict['min'].get()) > int(self.dict['max'].get()):
                self.dict['min'].delete(0, 'end')
                return False
        return True
    def clean_display(self):
        self.save_settings()
        for child in self.frame.winfo_children():
            child.destroy()
        self.dict = {}
        self.row = 0
    def save_settings(self):
        if self.validate_input():
            temp = {}
            for k, v in self.dict.items():
                temp[k] = v.get()
#                print(temp[k])
                self.config[self.text] = temp
    def write_settings(self):
        #DEBUG
        print("Saving")
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
    def read_settings(self):
        self.config.read('config.ini')
    def on_closing(self, *args):
        self.save_settings()
        self.write_settings()
        self.window.destroy()
    def cancel_closing(self, *args):
        self.window.destroy()
