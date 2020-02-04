import os
from flask import Flask, request

import telebot
from timetable import TimeTable
from scraper import load_timetable, give_link
import json

TOKEN = '1083066191:AAGXKSutCPElXS_jRbtmjZnShXbNItPps0k'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

users = {}
groups = []
day_command = ["today", "tomorrow", "yesterday", "week"]
shape_command = ["brief", "detail"]

from datetime import datetime

time = datetime.today().time()

hour = 18
minut = 15
flag = True
if time.hour == hour and time.minute == minut and flag:
    for key in users.keys():
        chat_id_= key
        break
    bot.send_message(chat_id_, text="Fuck, I don't belive that it work")
    flag == False
    


def is_day(sub_command, timetable):
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

@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    text = "I can help you to remember the timetable in  your university, \
current number of study-week and full name of your teacher\n\n\
You can control me by sending these commands:\n\n\
/timetable-show timetable in form and \
period of time what you like, for more information use command\n\
/help_timetable\n\
/week-show current number of study-week\n\
/name-show full name of teacher which\
your choice"
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['help_timetable'])
def help_timetable(message):
    chat_id = message.chat.id
    text = "Full command /timetable also contain two parameters\n -form\
in which you want to see the timeable (\"brief\" or \"detail\")\n -day or period\
of time in which about you want to know (\"today\", \
\"yesterday\", \"tomorrow\", \"week\", or \
any day on week: \"Monday\", \"Tuesday\", \"Wednesday\", etc.\n\
 You can write this parameters\
in any order what you like or pass any of them. By default, form is brief and\
 day is today. For example command \n/timetable detail week\n show you \
 timetable in detail, command"
    bot.send_message(chat_id, text)

    
@bot.message_handler(commands=['timetable'])
def timetable(message):
    chat_id = message.chat.id
    try:
        group = users[chat_id]
    except:
        text = "Probably you are new user, or bot was reload. Try to use \
 /group [your group] command"
        bot.send_message(chat_id, text=text)
        return None
    file_path = "TimeTabeles/{}".format(group) + ".json" 
    t = TimeTable(file_path)
    command = message.text.split()
    shape = "brief"
    day = "today"
    week = "current"
    if is_timetable_command(command, t):
        for sub_command in command:
            if is_day(sub_command, t):
                day = sub_command
            if is_shape(sub_command):
                shape = sub_command
        if day == "week":
            text = t.print_week(shape, week)
        else:
            text = t.print_day(t.give_day(day), shape, week)
            if text:
                text = day + '\n' + text
            else:
                text = "В этот день нет пар"
    else:
        text = "Command error"
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['week'])
def week(message):
    chat_id = message.chat.id
    file_curent_week = "current_week.json"
    with open(file_curent_week) as f:
        curent_week = json.load(f)
    bot.send_message(chat_id, text=curent_week)

@bot.message_handler(commands=['group'])
def group_(message):
    chat_id = message.chat.id
    try:
        group = message.text.split()[1]
    except:
        text = "Command error"
    if group in groups:
        users[chat_id] = group
        text = "Okay, now you can look on your timetable"
    else:
        try:
            time_table_update(group)
            users[chat_id] = group
            groups.append(group)
            text = "Okay, now you can look on your timetable"
        except:
            text = "Your group is probably wrong"
    bot.send_message(chat_id, text=text)
    
@bot.message_handler(commands=['update'])
def update(message):
    chat_id = message.chat.id
    try:
        group = users[chat_id]
    except:
        text = "Probably you are new user, or bot was reload. Try to use \
 /group [your group] command"
        bot.send_message(chat_id, text=text)
        return None
    time_table_update(group)
    text = "Your timetable successful"
    bot.send_message(chat_id, text=text)
    


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://stormy-falls-05476.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))