#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import botlog
import logging
import naver as n
import pickle
import romanizator as r

command_errors = {
    'ko': {
        'en': 'Use /english <text>',
        'zh-CN': 'Use /korean_chinese <text>'
    },
    'en': {'ko': 'Use /korean <text>'},
    'zh-CN': {'ko': 'Use /chinese_korean <text>',
    'romanize': 'Use /romanize <text>'}
}


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    botlog.log_activity(update)
    start_message = "🇰🇷 Welcome to the Hangul Bot, {} 🇰🇷\n\n".format(update.message.chat.first_name)
    start_message += "I can help you with romanization and translations!\n\n\n"
    # start_message += "🇰🇷 한글봇에 오신걸 환영합니다 🇰🇷\n\n"
    # start_message += "제가 로마자 표기법과 통역을 도와 드릴수 있어요!\n"
    bot.send_message(chat_id=update.message.chat_id, text=start_message)


def romanize(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    romanizator = r.Romanizator()

    if message == '':
        message = command_errors['romanize']
    else:
        if (romanizator.has_hangul(message)):
            message = romanizator.romanize(message)
        else:
            message = "There's no hangul in this message 🤔"

    update.message.reply_text(message, quote=True)


def translate(source, target, text):
    if text == '':
        return command_errors[source][target]

    naver = n.Naver()
    return naver.translate(source, target, text)


def english(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    update.message.reply_text(translate('ko', 'en', message), quote=True)


def korean(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    update.message.reply_text(translate('en', 'ko', message), quote=True)


def chinese_korean(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    update.message.reply_text(translate('zh-CN', 'ko', message), quote=True)


def korean_chinese(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    update.message.reply_text(translate('ko', 'zh-CN', message), quote=True)


def echo(bot, update):
    botlog.log_activity(update)
    romanizator = r.Romanizator()

    if (romanizator.has_hangul(update.message.text)):
        message = romanizator.romanize(update.message.text)
        update.message.reply_text(message, quote=True)


def unknown(bot, update):
    botlog.log_activity(update)
    message = """Sorry, I didn't understand your command! Are you a North Korean spy?! 🇰🇵\
    \n\nhttps://youtu.be/EFwitVDo540"""
    update.message.reply_text(message, quote=True)


def help(bot, update):
    botlog.log_activity(update)
    message = """
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

If you send me any message within Hangul, I will romanize it.

Wait for news!

If you have any questions or suggestions – or money to give 💰–, ping my <b>beloved master</b> @vafjr87"""

    update.message.reply_text(message, quote=True)


def main():
    with open('token', 'rb') as token:
        token = pickle.load(token)

    updater = Updater(token=token.get('telegram'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('romanize', romanize, pass_args=True))
    dp.add_handler(CommandHandler('english', english, pass_args=True))
    dp.add_handler(CommandHandler('English', english, pass_args=True))
    dp.add_handler(CommandHandler('Korean', korean, pass_args=True))
    dp.add_handler(CommandHandler('korean', korean, pass_args=True))
    dp.add_handler(CommandHandler('chinese_korean', chinese_korean, pass_args=True))
    dp.add_handler(CommandHandler('Chinese_korean', chinese_korean, pass_args=True))
    dp.add_handler(CommandHandler('korean_chinese', korean_chinese, pass_args=True))
    dp.add_handler(CommandHandler('Korean_chinese', korean_chinese, pass_args=True))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print('Start Time:\t{}\t@hangul_bot is running! 한글 봇 만세! '.format(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
    main()
    print('End Time:\t{}\t@hangul_bot is running! 한글 봇 만세! '.format(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
