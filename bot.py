# coding=utf-8
from telegram.ext import Updater, InlineQueryHandler, \
    MessageHandler, CommandHandler
from telegram.ext.filters import Filters
import requests
import re
from utils import *

import logging


def start(bot, update):
    start_msg = """
    Hi! I am bot specifically designed to track \
    and notify you about new subscribers/unsubscribers in your channel. \
    Before I can do that, please do the following:

    1) Add me as an admin to your channel

    2) After that, send me the name/URL of your channel

    """
    update.message.reply_text(start_msg)


def bop(bot, update):
    channel_name = update.message.text
    chat_id = update.message.chat_id

    if channel_name[0] == "@":
        channel_name = channel_name[1:]

    if channel_name.startswith("http://"):
        channel_name = channel_name[7:]

    if channel_name.startswith("https://"):
        channel_name = channel_name[8:]

    if channel_name.startswith("t.me/"):
        channel_name = channel_name[5:]

    channel_name = channel_name.lower()

    try:
        subs = get_subscribers_list(channel_name)
        try:
            add_tracking_channel(chat_id, channel_name)
            success = "Your channel was accepted!"
            bot.send_message(chat_id=chat_id, text=success)
        except Exception:
            channel_exist = "Are you sure you didn't add this channel before?"
            bot.send_message(chat_id=chat_id, text=channel_exist)
    except Exception:
    	admin_right = """Something went wrong. \
            Are you sure bot was added as an admin \
            and you gave me the right name of the channel?"""
        bot.send_message(chat_id=chat_id, text=admin_right)


def main():
    updater = Updater(get_token())
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, bop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
