#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import naver as n
import pickle
import romanizator as r


def start(bot, update):
    start_message = "🇰🇷 Welcome to the Hangul Bot 🇰🇷\n\n"
    start_message += "I can help you with romanization and translations\n\n\n"
    start_message += "🇰🇷 한글봇에 오신걸 환영합니다 🇰🇷\n\n"
    start_message += "제가 로마자 표기법과 통역을 도와 드릴수 있어요!\n"
    bot.send_message(chat_id=update.message.chat_id, text=start_message)


def romanize(bot, update, args):
    message = ' '.join(args)
    romanizator = r.Romanizator()

    if (romanizator.has_hangul(message)):
        message = romanizator.romanize(message)
    else:
        message = "There's no hangul in this message 🤔"

    bot.send_message(chat_id=update.message.chat_id, text=message)


def translate(source, target, text):
    naver = n.Naver()
    return naver.translate(source, target, text)


def english(bot, update, args):
    message = ' '.join(args)
    update.message.reply_text(translate('ko', 'en', message))


def korean(bot, update, args):
    message = ' '.join(args)
    update.message.reply_text(translate('en', 'ko', message))


def chinese_korean(bot, update, args):
    message = ' '.join(args)
    update.message.reply_text(translate('zh-CN', 'ko', message))


def korean_chinese(bot, update, args):
    message = ' '.join(args)
    update.message.reply_text(translate('ko', 'zh-CN', message))


def echo(bot, update):
    romanizator = r.Romanizator()

    if (romanizator.has_hangul(update.message.text)):
        message = romanizator.romanize(update.message.text)
        update.message.reply_text(message)


def unknown(bot, update):
    text = """Sorry, I didn't understand your command! Are you a North Korean spy?! 🇰🇵\
    \nhttps://youtu.be/EFwitVDo540"""
    bot.send_message(chat_id=update.message.chat_id, text=text)


def help(bot, update):
    help_message = """
Hello! I am the Hangul Bot! 🇰🇷

How can I help you now?

Currently I understand these commands:

Translations (powered by Naver®):

/korean <text>: 🇺🇸 → 🇰🇷
/english <text>:  🇰🇷 → 🇺🇸
/korean_chinese <text>: 🇰🇷 → 🇨🇳
/chinese_korean <text>: 🇨🇳→ 🇰🇷

Other commands:

/romanize <text>:  romanize Hangul sentences

If you send me any text within Hangul, I will romanize it.

Wait for news!

If you have any questions or suggestions or money to give 💰, ping @vafjr87."""

    bot.send_message(chat_id=update.message.chat_id, text=help_message)


if __name__ == '__main__':
    with open('token', 'rb') as token:
        token = pickle.load(token)

    updater = Updater(token=token.get('telegram'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('romanize', romanize, pass_args=True))
    dispatcher.add_handler(CommandHandler('english', english, pass_args=True))
    dispatcher.add_handler(CommandHandler('English', english, pass_args=True))
    dispatcher.add_handler(CommandHandler('Korean', korean, pass_args=True))
    dispatcher.add_handler(CommandHandler('korean', korean, pass_args=True))
    dispatcher.add_handler(CommandHandler('chinese_korean', chinese_korean, pass_args=True))
    dispatcher.add_handler(CommandHandler('Chinese_korean', chinese_korean, pass_args=True))
    dispatcher.add_handler(CommandHandler('korean_chinese', korean_chinese, pass_args=True))
    dispatcher.add_handler(CommandHandler('Korean_chinese', korean_chinese, pass_args=True))
    dispatcher.add_handler(CommandHandler('help', help))

    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    print('@hangul_bot is running! 한글 봇 만세! ')
    updater.start_polling()
    updater.idle()
