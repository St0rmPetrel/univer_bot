#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 06:03:09 2020

@author: telman
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

import json

def is_lesson(lesson_name):
    for les in lesson_name:
        if les:
            return True
    return False
def is_puls(lesson_name):
    if len(lesson_name) == 1:
        return False
    else:
        return True
def lesson_dict(lesson_name, lesson_items):
    if lesson_items:
        lesson_dic = {}
        lesson_dic["Subject"] = lesson_name
        lesson_dic["Room"] = lesson_items[1]
        lesson_dic["Type"] = lesson_items[0]
        lesson_dic["Teacher"] = lesson_items[2]
    else:
        lesson_dic = None
    return lesson_dic
def filter_lesson_items(lesson_items):
    if lesson_items:
        lesson_items = [item.get_text() for item in lesson_items]
        if lesson_items[2]:
            lesson_items[2] = " ".join(lesson_items[2].split("\xa0"))
        return lesson_items
    else:
        return None
def filter_lesson(lesson_name, lesson_items):
    if is_lesson(lesson_name):
        if not is_puls(lesson_name):
            lesson_items = lesson_items[0]
            lesson_items = filter_lesson_items(lesson_items)
            lesson_name_q = lesson_name[0].get_text()
        else:
            lesson_name_q = [None, None]
            for i in range(2):
                lesson_items[i] = filter_lesson_items(lesson_items[i])
                if lesson_name[i]:
                    lesson_name_q[i] = lesson_name[i].get_text()
                else:
                    lesson_name_q[i] = None
        return (lesson_name_q, lesson_items)

def save_lesson(timetable, lesson, day, lesson_number, lesson_name):
    if is_lesson(lesson_name):
        lesson_name_q = lesson[0]
        lesson_items = lesson[1]
        if not is_puls(lesson_name):
            timetable[day][lesson_number] = lesson_dict(lesson_name_q, lesson_items)
        else:
            lesson_dic1 = lesson_dict(lesson_name_q[0], lesson_items[0])
            lesson_dic2 = lesson_dict(lesson_name_q[1], lesson_items[1])
            timetable[day][lesson_number] = [lesson_dic1, lesson_dic2]    
    

def take_timetable(bs):
    week_days = ["Понедельник", "Вторник", "Среда",
             "Четверг", "Пятница", "Суббота"]
    lesson_time = ["08:30 - 10:05", "10:15 - 11:50", "12:00 - 13:35", 
               "13:50 - 15:25", "15:40 - 17:15", 
               "17:25 - 19:00", "19:10 - 20:45"]
    timetable = {}
    for day in week_days:
        day_pars = bs.find(text=day).findPrevious(name="tbody")
        timetable[day] = [None, None, None, None, None, None, None]
        lesson_number = 0
        for time in lesson_time:
            lesson = day_pars.find(text=time).findPrevious(name="tr")
            lesson = lesson.findAll("td")[1:]
            lesson_name = [sub.find("span") for sub in lesson]
            lesson_items = [sub.findAll("i") for sub in lesson]
            lesson_q = filter_lesson(lesson_name, lesson_items)
            save_lesson(timetable, lesson_q, day, lesson_number, lesson_name)
            lesson_number += 1
    timetable["Воскресенье"] = [None, None, None, None, None, None, None]
    return timetable    

def save_json(new_file_name, data):
    with open(new_file_name, 'w') as f:
        json.dump(data, f)
        
def give_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def load_timetable(url, new_file_name):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    timetable = take_timetable(bs)
    save_json(new_file_name, timetable)

def load_week(url, new_file_name):
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    data = bs.h4.get_text()
    save_json(new_file_name, data)
    
def give_link(group):
    url = "https://students.bmstu.ru/schedule/list"
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    link = bs.find(text=re.compile(group)).parent["href"]
    link = "https://students.bmstu.ru{}".format(link)
    return link