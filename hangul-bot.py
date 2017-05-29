#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import romanizator as roman
import logging
import sys


def start(bot, update):
    start_message =  "🇰🇷 Welcome to the Hangul Bot 🇰🇷\n\n"
    start_message += "We're still under construction, but you're able to use the /romanize <text>\n"
    start_message += "Try to romanize some koreans sentences!\n\n"
    start_message += "🇰🇷 한글봇에 오신걸 환영합니다 🇰🇷\n\n"
    start_message += "아직 개발중에 있지만 /romanize 커맨드를 쓰실수 있습니다\n"
    start_message += "아무 문장이나 로마자 표기법으로 바꿔보세요!"
    bot.send_message(chat_id=update.message.chat_id, text=start_message)


def romanize(bot, update, args):
    message = ' '.join(args)
    r = roman.Romanizator()

    if (r.has_hangul(message)):
        message = r.romanize(message)
    else:
        message = "There's no hangul in this message 🤔"

    bot.send_message(chat_id=update.message.chat_id, text=message)


def echo(bot, update):
    r = roman.Romanizator()

    if (r.has_hangul(update.message.text)):
        message = r.romanize(update.message.text)
        bot.send_message(chat_id=update.message.chat_id, text=message)


def unknown(bot, update):
    text = """Sorry, I didn't understand that! Are you a North Korean spy?! 🇰🇵\nTry /romanize <text>"""
    bot.send_message(chat_id=update.message.chat_id, text=text)

def help(bot, update):
    help_message =  """
Hello! I am the Hangul Bot! 🇰🇷

What can I help you now? Mmmm..., okay:

Well... currently I only can romanize Hangul sentences

Send me any message with Hangul within and I'll handle it (with /romanize in groups)

Wait for news!

If you have any questions or suggestions, send @vafjr87 a message."""

    bot.send_message(chat_id=update.message.chat_id, text=help_message)


if __name__ == '__main__':
    updater = Updater(token=sys.argv[1])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('romanize', romanize, pass_args=True))
    dispatcher.add_handler(CommandHandler('help', help))
    
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    print('Hangul Bot is running! Hooray! 🤗')
    updater.start_polling()