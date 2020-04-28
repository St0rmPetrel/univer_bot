#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 09:05:32 2020

@author: telman
"""
from scraper import load_timetable, give_link, load_week

day_command = ["today", "tomorrow", "yesterday", "week"]
shape_command = ["brief", "detail"]

def is_day(sub_command, timetable):
    """Say is a day or not."""
    if sub_command in (timetable.weekdays + day_command):
        return True
    else:
        return False

def is_shape(sub_command):
    if sub_command in shape_command:
        return True
    else:
        return False
def is_timetable_command(command, timetable):
    if command[0] == "/timetable":
        if len(command) > 1:
            command = command[1:]
            flag = True
            for sub_command in command:
                if is_day(sub_command, timetable) or is_shape(sub_command):
                    pass
                else:
                    flag = False
            if flag:
                return True
            else:
                return False
        else:
            return True
    else:
        return False
    
def time_table_update(group):
    link = give_link(group)
    file_path = "TimeTabeles/{}".format(group) + ".json"
    load_timetable(link, file_path)
    return file_path

def week_update(group):
    link = give_link(group)
    file_path = "current_week.json"
    load_week(link, file_path)
    return file_path

def text_messege(command):
    text_start = "I can help you to remember the timetable in  your university and \
current number of study-week.\n\n\
You can control me by sending these commands:\n\n\
/group [your group] if you are a new user it's set up your group.\
For example command \n/group СМ4-91\n set up your group on СМ4-91\n\
/timetable-show timetable in form and \
period of time what you like, for more information use command\n\
/help_timetable\n\
/update - update your timetable according on site bmstu\n\
/week-show current number of study-week\n\
/newweek - update your current week according on site bmstu"
    text_help_timetable = "Full command /timetable also contain two parameters\n -form \
in which you want to see the timeable (\"brief\" or \"detail\")\n -day or period\
of time in which about you want to know (\"today\", \
\"yesterday\", \"tomorrow\", \"week\", or \
any day on week: \"Monday\", \"Tuesday\", \"Wednesday\", etc.\n\
 You can write this parameters\
in any order what you like or pass any of them. By default, form is brief and\
 day is today. For example command \n/timetable detail week\n show you \
 timetable in detail, command"
    dic = {"start":text_start, "help_timetable":text_help_timetable}
    try:
        ans = dic[command]
    except:
        ans = ""
    return ans
 