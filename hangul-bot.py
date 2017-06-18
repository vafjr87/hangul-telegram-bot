#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import botlog
import logging
import naver as n
import pickle
import romanizator as r
import telegram

command_errors = {
    'ko': {
        'en': 'Use /english <i>text</i>',
        'zh-CN': 'Use /korean_chinese <i>text</i>'
    },
    'en': {'ko': 'Use /korean <i>text</i>'},
    'zh-CN': {'ko': 'Use /chinese_korean <i>text</i>'},
    'romanize': 'Use /romanize <i>text</i>',
    'none': 'Sorry. I failed. Please try again!',
    'no_hangul': "There's no hangul in this message 🤔"
}


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    botlog.log_activity(update)
    start_message = "🇰🇷 Welcome to the <i>Hangul Bot</i>, {} 🇰🇷\n\n".format(update.message.chat.first_name)
    start_message += "I can help you with <b>translations</b> and <b>romanization!</b>\n"
    start_message += "Press /help to learn my commands\n\n\n"
    start_message += "🇰🇷 <i>한글봇</i>에 오신걸 환영합니다 🇰🇷\n\n"
    start_message += "<b>번역</b>과 <b>로마자 표기법</b>을 도와 드릴수 있어요!\n"
    start_message += "커맨드를 보실려면 /help 를 눌러주세요."
    bot.send_message(chat_id=update.message.chat_id, text=start_message,
        parse_mode=telegram.ParseMode.HTML)


def romanize(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    romanizator = r.Romanizator()

    if message == '':
        result = {'message': command_errors['romanize'], 'parse': telegram.ParseMode.HTML}
    else:
        if (romanizator.has_hangul(message)):
            result = {'message': romanizator.romanize(message)}
        else:
            result = {'message': command_errors['no_hangul']}

    if result.get('parse'):
        update.message.reply_text(result['message'], quote=True, parse_mode=result['parse'])
    else:
        update.message.reply_text(result['message'], quote=True)


def translate(source, target, text):
    if text == '':
        return {'message': command_errors[source][target], 'parse': telegram.ParseMode.HTML}

    naver = n.Naver()
    result = naver.translate(source, target, text)
    if result is not None:
        return {'message': result}
    else:
        return {'message': command_errors['none']}


def english(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    result = translate('ko', 'en', message)
    if result.get('parse'):
        update.message.reply_text(result['message'], quote=True, parse_mode=result['parse'])
    else:
        update.message.reply_text(result['message'], quote=True)


def korean(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    result = translate('en', 'ko', message)
    if result.get('parse'):
        update.message.reply_text(result['message'], quote=True, parse_mode=result['parse'])
    else:
        update.message.reply_text(result['message'], quote=True)


def chinese_korean(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    result = translate('zh-CN', 'ko', message)
    if result.get('parse'):
        update.message.reply_text(result['message'], quote=True, parse_mode=result['parse'])
    else:
        update.message.reply_text(result['message'], quote=True)


def korean_chinese(bot, update, args):
    botlog.log_activity(update)
    message = ' '.join(args)
    result = translate('ko', 'zh-CN', message)
    if result.get('parse'):
        update.message.reply_text(result['message'], quote=True, parse_mode=result['parse'])
    else:
        update.message.reply_text(result['message'], quote=True)


def echo(bot, update):
    botlog.log_activity(update)
    romanizator = r.Romanizator()

    if (romanizator.has_hangul(update.message.text)):
        result = translate('ko', 'en', update.message.text)
    else:
        result = translate('en', 'ko', update.message.text)

    update.message.reply_text(result['message'], quote=True)


def unknown(bot, update):
    botlog.log_activity(update)
    message = """Sorry, I didn't understand your command! Are you a <b>North Korean spy?!</b> 🇰🇵\
    \n\nhttps://youtu.be/EFwitVDo540"""
    update.message.reply_text(message, quote=True, parse_mode=telegram.ParseMode.HTML)


def help(bot, update):
    botlog.log_activity(update)
    message = """
Hello! I am the Hangul Bot! 🇰🇷

How can I help you now?

Currently I understand these commands:

Translations (powered by Naver®):

/korean <i>text:</i> 🇺🇸 → 🇰🇷
/english <i>text:</i>  🇰🇷 → 🇺🇸
/korean_chinese <i>text:</i> 🇰🇷 → 🇨🇳
/chinese_korean <i>text:</i> 🇨🇳→ 🇰🇷

Other commands:

/romanize text:  romanize Hangul sentences

If you send me any message within Hangul, I will translate it to English, but, it's an English message, I will translate it to Korean!

Wait for news!

If you have any questions or suggestions – or money to give 💰–, ping my <b>beloved master</b> @vafjr87"""

    update.message.reply_text(message, quote=True, parse_mode=telegram.ParseMode.HTML)


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
