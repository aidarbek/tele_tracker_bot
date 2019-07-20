# coding=utf-8
from pyrogram import Client
import time
from celery import Celery
import pickle
import mysql.connector


def get_token():
    return ""


def get_bot_name():
    return ""


def get_db_config():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tracker',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    return config


def get_tracking_channels():
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT owner, bot FROM tracker')
        results = [(owner, bot) for (owner, bot) in cursor]
        cursor.close()
        connection.close()
        return results
    except Exception:
        return []


def get_subs(target):
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM subs WHERE bot='{}'".format(target))
        results = []
        results = [(row[0], row[1]) for row in cursor]
        cursor.close()
        connection.close()
        return results
    except Exception:
        return []


def add_sub(name, target, uuid):
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = "INSERT INTO subs (name, bot, id) VALUES (%s,%s,%s)"
    result = cursor.execute(sql, (name, target, uuid))
    connection.commit()
    cursor.close()
    connection.close()


def delete_sub(uuid, target):
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = "DELETE FROM subs WHERE id=%s and bot=%s"
    result = cursor.execute(sql, (uuid, target))
    connection.commit()
    cursor.close()
    connection.close()


def add_tracking_channel(owner, bot):
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = "INSERT INTO tracker (owner, bot) VALUES ({}, '{}')"\
        .format(owner, bot)
    result = cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

app = Client(get_bot_name(), bot_token=get_token())


def name(member):
    if isinstance(member, str):
        return member
    res = ""
    if member.first_name:
        res += member.first_name + " "
    if member.last_name:
        res += member.last_name + " "
    if member.username:
        res += "("+member.username+")"
    return res

def get_all_subscribers_list(target):
    bot = TelegramClient('bot', get_api_id(), get_api_hash()).start(bot_token=get_token())
    with bot:
        bot.connect()
        res = []
        all_participants = bot.get_participants(target, aggressive=True)
        for user in all_participants:
            res.append((user.id, name(user)))
        return res
