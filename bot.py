import os
from flask import Flask, request

import telebot
from timetable import TimeTable
import json

TOKEN = '1083066191:AAGXKSutCPElXS_jRbtmjZnShXbNItPps0k'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

day_command = ["today", "tomorrow", "yesterday", "week"]
shape_command = ["brief", "detail"]

def is_day(sub_command, timetable):
    if sub_command in (timetable.weekdays + day_command):
        return True
    else:
        return False
def is_shape(sub_command, timetable):
    if sub_command in shape_command:
        return True
    else:
        return False

@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    text = "I can help you to remember the timetable in  your university, \
current number of study-week and full name of your teacher\n\n\
You can control me by sending these commands:\n\n\
/timetable-show timetable in form and \
period of time what you like\n\
/week-show current number of study-week\n\
/name-show full name of teacher which\
your choice"
    bot.send_message(chat_id, text)    

    
@bot.message_handler(commands=['timetable'])
def timetable(message):
    chat_id = message.chat.id
    t = TimeTable("old_timetable.json")
    #command = message.text
    text = t.print_days("week")
    text += '\n' + message.text
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['week'])
def week(message):
    chat_id = message.chat.id
    file_curent_week = "current_week.json"
    with open(file_curent_week) as f:
        curent_week = int(json.load(f))
    bot.send_message(chat_id, text=curent_week)
    


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