# Main imports for server.
import os
from flask import Flask, request
import telebot
# My imports 
from timetable import TimeTable
from handler import *

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

users = {}#
groups = []#

@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    text = text_messege('start')
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['help_timetable'])
def help_timetable(message):
    chat_id = message.chat.id
    text = text_messege('help_timetable')
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
    groups = give_json("groups.json")
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
    # save_json("users.json", users)
    # save_json("groups.json", groups)
    bot.send_message(chat_id, text=text)
    
@bot.message_handler(commands=['update'])
def update(message):
    chat_id = message.chat.id
    # users = give_json("users.json")
    try:
        group = users[chat_id]
    except:
        text = "Probably you are new user, or bot was reload. Try to use \
 /group [your group] command"
        bot.send_message(chat_id, text=text)
        return None
    time_table_update(group)
    text = "Your timetable was updating successful"
    bot.send_message(chat_id, text=text)

@bot.message_handler(commands=['newweek'])
def newweek(message):
    chat_id = message.chat.id
    try:
        group = users[chat_id]
    except:
        text = "Probably you are new user, or bot was reload. Try to use \
 /group [your group] command"
        bot.send_message(chat_id, text=text)
        return None
    week_update(group)
    text = "Your week was updating successful"
    bot.send_message(chat_id, text=text)

# From this place start server part, don't touch.
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
