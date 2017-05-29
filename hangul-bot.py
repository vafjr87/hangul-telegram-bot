#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import romanizator as roman
import logging
import sys

def start(bot, update):
    start_text =  "🇰🇷 Welcome to the Hangul Bot 🇰🇷\n\n"
    start_text += "We're still under construction, but you're able to use the /romanize <text>\n"
    start_text += "Try to romanize some koreans sentences!\n\n"
    start_text += "🇰🇷 한글봇에 오신걸 환영합니다 🇰🇷\n\n"
    start_text += "아직 개발중에 있지만 /romanize 커맨드를 쓰실수 있습니다\n"
    start_text += "아무 문장이나 로마자 표기법으로 바꿔보세요!"
    bot.send_message(chat_id=update.message.chat_id, text=start_text)


def romanize(bot, update, args):
    message = ' '.join(args)
    r = roman.Romanizator()

    if (r.has_hangul(message)):
        message = r.romanize(message)
    else:
        message = "There's no hangul in this message 🤔"

    bot.send_message(chat_id=update.message.chat_id, text=message)


def unknown(bot, update):
    text = """Sorry, I didn't understand that command 😭\nTry /romanize <text>"""
    bot.send_message(chat_id=update.message.chat_id, text=text)


if __name__ == '__main__':
    updater = Updater(token=sys.argv[1])
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('romanize', romanize, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    print('Hangul Bot is running! Hooray! 🤗')
    updater.start_polling()