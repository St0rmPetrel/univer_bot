#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 13:15:44 2020

@author: telman
"""

from telegram.ext import MessageHandler, Filters

from markups import (HELP, help_menu_markup)

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

def help_main(update, context):
    update.message.reply_text("Enter in help menu", 
                              reply_markup=help_menu_markup)
    return HELP
reg_str = r'^(help)$'
help_main_handler = MessageHandler(Filters.regex(reg_str), help_main)
# >>>>> HELP functions >>>>>
def help_timetable(update, context):
    update.message.reply_text("Enter in: help_timetable")
 
reg_str = r'^(timetable)$'
help_timetable_handler = MessageHandler(Filters.regex(reg_str), 
                                        help_timetable)

def help_week(update, context):
    update.message.reply_text("Enter in: help_week")
    
reg_str = r'^(week)$'
help_week_handler = MessageHandler(Filters.regex(reg_str), 
                                        help_week)

def help_update(update, context):
    update.message.reply_text("Enter in: help_update")
    
reg_str = r'^(update)$'
help_update_handler = MessageHandler(Filters.regex(reg_str), 
                                        help_update)

def help_admin(update, context):
    update.message.reply_text("Enter in: help_admin")
    
reg_str = r'^(admin)$'
help_admin_handler = MessageHandler(Filters.regex(reg_str), 
                                        help_admin)

# <<<< HELP functions <<<<<