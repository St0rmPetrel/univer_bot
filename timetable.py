"""
Created on Wed Jan 29 08:48:23 2020

@author: Telman
"""
import json
from datetime import datetime, timedelta

class TimeTable():
    """
    bla bla bla 
    """
    
    def __init__(self, filename="timetable.json", 
                 file_curent_week="current_week.json"):
        """
        Parameters
        ----------
        filename : Str
            Name *.json file where store the timetable.
        -------
        None.

        """
        self.filename = filename
        with open(self.filename) as f:
            self.timetable = json.load(f)
        self.file_curent_week = file_curent_week
        with open(self.file_curent_week) as f:
            self.curent_week = int(json.load(f).split()[0])
        self.lesson_time = ["08:30 - 10:05", "10:15 - 11:50", "12:00 - 13:35", 
                            "13:50 - 15:25", "15:40 - 17:15", 
                            "17:25 - 19:00", "19:10 - 20:45"]
        self.weekdays = ["Monday", "Teusday", "Wednesday", "Thursday", 
                         "Friday", "Saturday", "Sunday"]
        
    def brief(self, lesson, lesson_number):
        time_beg = self.lesson_time[lesson_number].split()[0]
        if lesson["Teacher"]:
            teacher = lesson["Teacher"].split()[0]
        else:
            teacher = lesson["Teacher"]
        line = " ".join((time_beg, teacher, lesson["Type"], lesson["Room"]))
        return line
    
    def detail(self, lesson, lesson_number):
        time = self.lesson_time[lesson_number]
        line = " ".join((time, lesson["Subject"], lesson["Teacher"], 
                         lesson["Type"]))
        return line
    
    def give_day(self, day):
        day_number = 6
        today = datetime.today()
        one_day = timedelta(days=1)
        if day.lower() == "today":
            day_number = today.weekday()
        elif day.lower() == "yesterday":
            yesterday = today - one_day
            day_number = yesterday.weekday()
        elif day.lower() == "tomorrow":
            tomorrow = today + one_day
            day_number = tomorrow.weekday()
        else:
            for i in range(7):
                if day.lower() == self.weekdays[i].lower():
                    day_number = i
        return self.timetable[self.weekdays[day_number]]
            
    def print_day(self, table_day, shape_form="brief", 
                  week="current"):
        if week == "current":
            week_number = self.curent_week
        else:
            week_number = int(week)
        week_odd = (week_number % 2) == 0
        text = ""
        lesson_number = 0
        if shape_form == "brief":
            shape = self.brief
        else:
            shape = self.detail
        for pare in table_day:
            if pare:
                if type(pare) == list:
                    if week_odd:
                        if pare[1]:
                            text += shape(pare[1], lesson_number) + '\n'
                    else:
                        if pare[0]:
                            text += shape(pare[0], lesson_number) + '\n'
                else:
                    text += shape(pare, lesson_number) + '\n'
            lesson_number += 1
        return text
    
    def print_week(self, shape_form="brief", week="current"):
        text = ""
        for day in self.weekdays:
            text_day = self.print_day(self.give_day(day), shape_form, week)
            if text_day:
                text += day + '\n'
                text += text_day + '\n'
        return text
   
