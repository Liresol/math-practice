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
    def get_avg_times(self):
        avgs = {}
        for k in self.totals:
            lst = []
            lst.append(self.totals[k][0]/self.totals[k][1])
            if self.totals[k][3] is not 0:
                lst.append(self.totals[k][2]/self.totals[k][3])
                #WARNING: MESSING WITH INFINITY
            else:
                lst.append(float('inf'))
            avgs[k] = lst
        return avgs

path = 'stats.json'
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
        except KeyError:
            print("No sessions done today")
        return ret
    def get_n_day_stats(n):
        ret = Stats()
        with open(path) as data_file:
            data = json.load(data_file)
        for i in get_last_n_days(n):
            try:
                ret.merge_stats(Stats(data[i]))
            except KeyError:
                pass
        return ret
    def get_week_stats():
        return get_n_day_stats(7)
    def get_30_day_stats():
        return get_n_day_stats(30)
    def get_90_day_stats():
        return get_n_day_stats(90)
    def get_year_stats():
        return get_n_day_stats(365)
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
        print(data)
        with open(path, "w") as outfile:
            json.dump(data, outfile)

class StatsDisplay:
    def __init__(self):
        pass
