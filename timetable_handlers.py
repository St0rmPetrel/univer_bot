#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 16:23:25 2020

@author: telman
"""
from telegram import ReplyKeyboardRemove
from telegram.ext import MessageHandler, Filters

from markups import (TIME_TABLE, FORMAT, DAY, WEEK_NUM, MAIN_MENU,
                     timetable_menu_markup, day_menu_markup, 
                     format_menu_markup, week_num_menu_markup,
                     main_menu_markup)

from timetable import TimeTable

from data_base_handler import (give_timetable, give_week)

def timetable_main(update, context):
    user_data = context.user_data
    user_data['DAY_OR_WEEK'] = 'today'
    user_data['FORMAT'] = 'brief'
    user_data['WEEK_NUM'] = 'current'
    update.message.reply_text("Enter in timetable menu", 
                              reply_markup=timetable_menu_markup)
    return TIME_TABLE

timetable_main_handler = MessageHandler(Filters.regex(r'^(timetable)$'), 
                                        timetable_main)

def timetable_week(update, context):
    context.user_data['DAY_OR_WEEK'] = 'week'
    update.message.reply_text("Set DAY_OR_WEEK = week")
    update.message.reply_text("Enter in timtable-format menu", 
                              reply_markup=format_menu_markup)
    return FORMAT

timetable_week_handler = MessageHandler(Filters.regex(r'^(week)$'), 
                                        timetable_week)

def timetable_day(update, context):
    update.message.reply_text("Enter in timtable-day-choise menu", 
                              reply_markup=day_menu_markup)
    return DAY

timetable_day_handler = MessageHandler(Filters.regex(r'^(day)$'), 
                                        timetable_day)

convert_dict = {'today': 'today', 'tomorrow': 'tomorrow', 
                'yesterday': 'yesterday',
                'Mon': "ПН",'Tues': "ВТ", 'Wed': "СР",
                'Thurs': "ЧТ", 'Fri': "ПТ", 'Sat': "СБ"}

def timetable_day_choise(update, context):
    day = update.message.text
    update.message.reply_text("Set DAY = {}".format(day))
    day = convert_dict[day]
    context.user_data['DAY_OR_WEEK'] = day
    update.message.reply_text("Enter in timtable-format menu", 
                              reply_markup=format_menu_markup)
    return FORMAT

reg_str = r'^(today|tomorrow|yesterday|Mon|Tues|Wed|Thurs|Fri|Sat)$'
days_handler = MessageHandler(Filters.regex(reg_str), timetable_day_choise)

def format_choise(update, context):
    timetable_format = update.message.text
    context.user_data['FORMAT'] = timetable_format
    update.message.reply_text("Set FORMAT = {}".format(timetable_format))
    update.message.reply_text("Enter in timtable-week-num menu", 
                              reply_markup=week_num_menu_markup)
    return WEEK_NUM

format_handler = MessageHandler(Filters.regex(r'^(brief|detail)$'), 
                                      format_choise)

def print_timetable(chat_id, day_or_week, timetable_format, week_num):
    data = give_timetable(chat_id)
    week = give_week()
    t = TimeTable(data, week)
    if day_or_week == 'week':
        text = t.print_week(timetable_format, week_num)
    else:
        text = t.print_day(t.give_day(day_or_week), timetable_format, week_num)
    return text

def week_convertor(week_num):
    if week_num == 'odd':
        week_num = 1
    elif week_num == 'even':
        week_num = 2
    return week_num
    
    
def week_num_choise(update, context):
    week_num = update.message.text
    chat_id = update.message.chat_id
    user_data = context.user_data
    update.message.reply_text("Set WEEK_NUM = {}".format(week_num),
                              reply_markup=ReplyKeyboardRemove())
    
    user_data['WEEK_NUM'] = week_convertor(week_num)
    text = print_timetable(chat_id, user_data['DAY_OR_WEEK'], user_data['FORMAT'],
                    user_data['WEEK_NUM'])
    update.message.reply_text(text)
    update.message.reply_text("Enter in main menu:", 
                              reply_markup=main_menu_markup)
    return MAIN_MENU

week_num_handler = MessageHandler(Filters.regex(r'^(current|odd|even)$'), 
                                      week_num_choise)
# <<< timetable stuff <<<