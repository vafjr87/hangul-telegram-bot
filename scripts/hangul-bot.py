# !/usr/bin/env python3
# -*- coding: utf-8 -*-
 
from datetime import datetime
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from romanizator import Romanizator

import logging
import telegram
# import sys
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    message = f'🇰🇷 Welcome to the *Hangul Bot*, {update.message.chat.first_name}!'

    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def echo(update: Update, context: CallbackContext) -> None:
    romanizator = Romanizator()

    if romanizator.has_hangul(update.message.text):
        update.message.reply_text(romanizator.romanize(update.message.text), quote=True)


def help(update: Update, context: CallbackContext) -> None:
    message = """
    I am the Hangul Bot, a * bot under maintenance*.\nYou can send me messages in Hangul and I will romanize them for you.
    """

    update.message.reply_text(message, quote=True, parse_mode=ParseMode.MARKDOWN)


def main():
    """Start the bot."""
    TOKEN = os.environ['TELEGRAM_HANGULBOT_TOKEN']

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print('@hangul_bot is running! 한글 봇 만세!')
    main()
    print('@hangul_bot is not running! 한글 봇 만세!')
