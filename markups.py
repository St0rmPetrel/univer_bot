#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 13:38:02 2020

@author: telman
"""
from telegram import (ReplyKeyboardMarkup)

(MAIN_MENU, HELP, REGISTING, TIME_TABLE, 
 DAY, FORMAT, WEEK_NUM, UPDATE, ADMIN, UPDATE_GROUP) = range(10)



main_menu_reply_keyboard = [['help'],
                            ['timetable'],
                            ['week'],
                            ['update'],
                            ['admin']]

help_menu_reply_keyboard = [['timetable'],
                            ['week'],
                            ['update'],
                            ['admin'],
                            ['main menu']]

timetable_menu_reply_keyboard = [['week'],
                                 ['day'],
                                 ['main menu']]

day_menu_reply_keyboard = [['today'],
                           ['tomorrow'],
                           ['yesterday'],
                           ['Mon', 'Tues', 'Wed'],
                           ['Thurs', 'Fri', 'Sat'],
                           ['main menu']]

format_menu_reply_keyboard = [['brief'],
                              ['detail'],
                              ['main menu']]

week_num_menu_reply_keyboard = [['current'],
                                ['even'],
                                ['odd'],
                                ['main menu']]

update_menu_reply_keyboard = [['update group'],
                              ['update week'],
                              ['main menu']]

admin_menu_reply_keyboard = [['main menu']]



main_menu_markup = ReplyKeyboardMarkup(main_menu_reply_keyboard, 
                                       one_time_keyboard=True)
help_menu_markup = ReplyKeyboardMarkup(help_menu_reply_keyboard)
timetable_menu_markup = ReplyKeyboardMarkup(timetable_menu_reply_keyboard, 
                                       one_time_keyboard=True)
day_menu_markup = ReplyKeyboardMarkup(day_menu_reply_keyboard, 
                                       one_time_keyboard=True)
format_menu_markup = ReplyKeyboardMarkup(format_menu_reply_keyboard, 
                                       one_time_keyboard=True)
week_num_menu_markup = ReplyKeyboardMarkup(week_num_menu_reply_keyboard, 
                                       one_time_keyboard=True)
update_menu_markup = ReplyKeyboardMarkup(update_menu_reply_keyboard)
admin_menu_markup = ReplyKeyboardMarkup(admin_menu_reply_keyboard)