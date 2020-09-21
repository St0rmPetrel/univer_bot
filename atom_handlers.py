#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 16:53:19 2020

@author: telman
"""
from telegram.ext import (MessageHandler, Filters, ConversationHandler, 
                          CommandHandler)
from telegram import ReplyKeyboardRemove
from markups import (REGISTING, MAIN_MENU, ADMIN, main_menu_markup,
                     admin_menu_markup)

from data_base_handler import (is_ex_user, add_user, give_week)

# >>> regist with start >>>
def start(update, context):
    chat_id = update.message.chat_id
    if (not is_ex_user(chat_id)):
        update.message.reply_text("Registering: enter your group")
        return REGISTING
    update.message.reply_text("Enter in main menu:", 
                              reply_markup=main_menu_markup)
    return MAIN_MENU

start_handler = CommandHandler('start', start)

def registing(update, context):
    message = update.message
    chat_id = message.chat_id
    group = message.text
    name = message.from_user.first_name
    text = add_user(chat_id, name, group)
    update.message.reply_text(text)
    update.message.reply_text("Enter in main menu:", 
                              reply_markup=main_menu_markup)
    return MAIN_MENU

registing_handler = MessageHandler(Filters.text, registing)
# <<< regist with start <<< 

def back_main_menu(update, context):
    update.message.reply_text("I'm back",
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("Enter in main menu:", 
                              reply_markup=main_menu_markup)
    return MAIN_MENU

back_main_menu_handler = MessageHandler(Filters.regex(r'^(main menu)$'), 
                                        back_main_menu)


def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

cancel_handler = MessageHandler(Filters.regex('^Cancel$'), cancel)

# >>> admin stuff >>>
def admin_main(update, context):
    update.message.reply_text("Enter in admin menu", 
                              reply_markup=admin_menu_markup)
    return ADMIN

admin_main_handler = MessageHandler(Filters.regex(r'^(admin)$'), 
                                     admin_main)
# <<< admin stuff <<<

# >>> week stuff >>>
def week(update, context):
    text = give_week()
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("Enter in main menu:", 
                              reply_markup=main_menu_markup)
    return MAIN_MENU

week_handler = MessageHandler(Filters.regex(r'^week$'), 
                                        week)
# <<< week stuff <<<