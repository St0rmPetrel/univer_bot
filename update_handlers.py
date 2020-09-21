#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 16:42:11 2020

@author: telman
"""
from telegram.ext import MessageHandler, Filters

from markups import UPDATE, UPDATE_GROUP, update_menu_markup

from data_base_handler import (update_user_group, give_group, load_week,
                               give_week)

# >>> update stuff <<<
def update_main(update, context):
    update.message.reply_text("Enter in update menu", 
                              reply_markup=update_menu_markup)
    return UPDATE

update_main_handler = MessageHandler(Filters.regex(r'^(update)$'), 
                                     update_main)

def update_group(update, context):
    update.message.reply_text("Enter new group")
    return UPDATE_GROUP
    
update_group_handler = MessageHandler(Filters.regex(r'^(update group)$'), 
                                     update_group)

def update_group_regist(update, context):
    message = update.message
    chat_id = message.chat_id
    new_group = message.text
    text = update_user_group(chat_id, new_group)
    update.message.reply_text(text)
    return UPDATE

update_group_regist_handler = MessageHandler(Filters.text, update_group_regist)

def update_week(update, context):
    chat_id = update.message.chat_id
    group = give_group(chat_id)
    load_week(group)
    week = give_week()
    update.message.reply_text(week)
    
update_week_handler = MessageHandler(Filters.regex(r'^(update week)$'), 
                                     update_week)
# >>> update stuff <<<