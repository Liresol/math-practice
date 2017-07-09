from tkinter import *
from tkinter import ttk
import json
import datetime
import copy

"""
Returns in ISO 8601 format the current day.
"""
def get_date():
    return datetime.date.today().isoformat()

"""
Returns in ISO 8601 format the day n days before today.
"""
def get_past_date(n):
    delta = datetime.timedelta(days=n)
    return datetime.date.today()-delta.isoformat()

"""
Returns a list of n dates in ISO 8601 format from n-1 days ago to today
"""
def get_last_n_days(n):
    delta = datetime.timedelta(days=1)
    day = datetime.date.today()
    dlist = []
    for i in range(n):
        dlist.append(day.isoformat())
        day -= delta
    return dlist



"""
A class for keeping track of the stats of a single session.
Stats are stored as a dict with the question type as the key
and the value as a list containing the following in order:
Total time, Total answers, Total time for correct answers,
Correct answers
"""
class Stats:
    def __init__(self, dict={}):
        self.totals = copy.deepcopy(dict)
    def add_time(self, type, time, correct):
        if type not in self.totals:
            self.totals[type] = [time, 1, 0, 0]
            if correct:
                self.totals[type][2] = time
                self.totals[type][3] = 1
        else:
            self.totals[type][0] += time
            self.totals[type][1] += 1
            if correct:
                self.totals[type][2] += time
                self.totals[type][3] += 1
    def get_dict(self):
        return self.totals
    """
    NO ERROR CHECKING
    """
    def set_dict(self, dict):
        self.totals = dict
    def merge_stats(self, s):
        for k in s.totals:
            if k in self.totals:
                for i in range(len(self.totals[k])):
                    self.totals[k][i] += s.totals[k][i]
            else:
                self.totals[k] = s.totals[k]
    def get_display_vals(self):
        avgs = {}
        for k in self.totals:
            lst = []
            if self.totals[k][1] is not 0:
                lst.append(self.totals[k][0]/self.totals[k][1])
                #WARNING: using inf may create problems
            else:
                lst.append(float('inf'))
            if self.totals[k][3] is not 0:
                lst.append(self.totals[k][2]/self.totals[k][3])
                #WARNING: using inf may create problems
            else:
                lst.append(float('inf'))
            avgs[k] = lst
            if self.totals[k][1] is not 0:
                lst.append(self.totals[k][3]/self.totals[k][1])
            else:
                lst.append(0)
        return avgs

path = 'stats.json'
"""
Records the stats of a session into a JSON file
Since there is only one set of stats at any time (for now),
everything is a static method
"""
class StatsWriter:
    """
    Returns a stats class representing today's stats.
    """
    def get_today_stats():
        ret = Stats()
        try:
            date = get_date()
            with open(path) as data_file:
                data = json.load(data_file)
            ret.set_dict(data[date])
        except (KeyError, TypeError) as e:
            print("No sessions done today")
        return ret
    def get_n_day_stats(n):
        ret = Stats()
        try:
            with open(path, "r") as infile:
                data = json.load(infile)
        except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
            print("No history data")
            data = {}
        for i in get_last_n_days(n):
            try:
                ret.merge_stats(Stats(data[i]))
            except (KeyError, TypeError) as e:
                pass
        return ret
    def write_session(stats):
        date = get_date()
        try:
            with open(path, "r") as infile:
                data = json.load(infile)
        except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
            print("No history data")
            data = {}
        day_stats = Stats()
        if date in data:
            day_stats.set_dict(data[date])
        day_stats.merge_stats(stats)
        data[date] = day_stats.get_dict()
        with open(path, "w") as outfile:
            json.dump(data, outfile)
    def delete_stats():
        with open(path, "w") as outfile:
            json.dump({}, outfile)
class StatsWindow:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(master)
        self.frame = ttk.Frame(self.window)
        self.window.title('Stats')
        self.dstats = StatsWriter.get_today_stats()
        self.wstats = StatsWriter.get_n_day_stats(7)
        self.stats_30 = StatsWriter.get_n_day_stats(30)
        self.stats_90 = StatsWriter.get_n_day_stats(90)
        self.stats_365 = StatsWriter.get_n_day_stats(365)

        self.timeslot = StringVar()
        self.selections = ttk.Combobox(self.window, textvariable = self.timeslot)
        self.selections.bind('<<ComboboxSelected>>', self.parse_display)
        self.selections['values'] = ("Today's Stats","Week's Stats","30 Day Stats","90 Day Stats","365 Day Stats")
        self.selections.grid()
        self.frame.grid()
        self.day_display()
    def parse_display(self, *args):
        self.clean_display()
        text = self.timeslot.get()
        if text == "Today's Stats":
            self.day_display()
        elif text == "Week's Stats":
            self.week_display()
        elif text == "30 Day Stats":
            self.thirty_display()
        elif text == "90 Day Stats":
            self.ninty_display()
        elif text == "365 Day Stats":
            self.year_display()
    def day_display(self, *args):
        r = 0
        avgs = self.dstats.get_display_vals()
        self.frame.grid()
        for k in avgs:
            label1 = ttk.Label(self.frame, text=k + " ", font="Helvetica 15 bold")
            label2 = ttk.Label(self.frame, text="Average time per answer: " + str(avgs[k][0]) + 's')
            label3 = ttk.Label(self.frame, text="Average time per correct answer: " + str(avgs[k][1])+ 's')
            label4 = ttk.Label(self.frame, text="Accuracy: " + str(100* avgs[k][2]) + "%")
            label1.grid(row = r)
            label2.grid(row = r+1)
            label3.grid(row = r+2)
            label4.grid(row = r+3)
            r += 4
    def week_display(self, *args):

        r = 0
        avgs = self.wstats.get_display_vals()
        self.frame.grid()
        for k in avgs:
            label1 = ttk.Label(self.frame, text=k + " ", font="Helvetica 15 bold")
            label2 = ttk.Label(self.frame, text="Average time per answer: " + str(avgs[k][0]) + 's')
            label3 = ttk.Label(self.frame, text="Average time per correct answer: " + str(avgs[k][1])+ 's')
            label4 = ttk.Label(self.frame, text="Accuracy: " + str(100* avgs[k][2]) + "%")
            label1.grid(row = r)
            label2.grid(row = r+1)
            label3.grid(row = r+2)
            label4.grid(row = r+3)
            r += 4
    def thirty_display(self, *args):
        r = 0
        avgs = self.stats_30.get_display_vals()
        self.frame.grid()
        for k in avgs:
            label1 = ttk.Label(self.frame, text=k + " ", font="Helvetica 15 bold")
            label2 = ttk.Label(self.frame, text="Average time per answer: " + str(avgs[k][0]) + 's')
            label3 = ttk.Label(self.frame, text="Average time per correct answer: " + str(avgs[k][1])+ 's')
            label4 = ttk.Label(self.frame, text="Accuracy: " + str(100* avgs[k][2]) + "%")
            label1.grid(row = r)
            label2.grid(row = r+1)
            label3.grid(row = r+2)
            label4.grid(row = r+3)
            r += 4

        pass
    def ninty_display(self, *args):
        r = 0
        avgs = self.stats_90.get_display_vals()
        self.frame.grid()
        for k in avgs:
            label1 = ttk.Label(self.frame, text=k + " ", font="Helvetica 15 bold")
            label2 = ttk.Label(self.frame, text="Average time per answer: " + str(avgs[k][0]) + 's')
            label3 = ttk.Label(self.frame, text="Average time per correct answer: " + str(avgs[k][1])+ 's')
            label4 = ttk.Label(self.frame, text="Accuracy: " + str(100* avgs[k][2]) + "%")
            label1.grid(row = r)
            label2.grid(row = r+1)
            label3.grid(row = r+2)
            label4.grid(row = r+3)
            r += 4

        pass
    def year_display(self, *args):
        r = 0
        avgs = self.stats_365.get_display_vals()
        self.frame.grid()
        for k in avgs:
            label1 = ttk.Label(self.frame, text=k + " ", font="Helvetica 15 bold")
            label2 = ttk.Label(self.frame, text="Average time per answer: " + str(avgs[k][0]) + 's')
            label3 = ttk.Label(self.frame, text="Average time per correct answer: " + str(avgs[k][1])+ 's')
            label4 = ttk.Label(self.frame, text="Accuracy: " + str(100* avgs[k][2]) + "%")
            label1.grid(row = r)
            label2.grid(row = r+1)
            label3.grid(row = r+2)
            label4.grid(row = r+3)
            r += 4
    def clean_display(self):
        for child in self.frame.winfo_children():
            child.destroy()

