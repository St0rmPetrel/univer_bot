import os

from flask import Flask, request

import telebot
from telebot import types

from timetable import TimeTable

TOKEN = '1083066191:AAGXKSutCPElXS_jRbtmjZnShXbNItPps0k'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    text = "I can help you to remember the timetable in  your university, \
current number of study-week and full name of your teacher\n\n\
You can control me by sending these commands:\n\n\
/timetable-show timetable in form and \
period of time what you like\n\
/week-show current number of study-week\n\
/name-show full name of teacher which\
your choice"
    bot.send_message(chat_id, text)
    
@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('hi'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)
    
@bot.message_handler(commands=['timetable'])
def simple_timetable(message):
    chat_id = message.chat.id
    t = TimeTable("old_timetable.json")
    text = t.print_days("week")
    bot.send_message(chat_id=chat_id, text=text)
    


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
