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
        cursor.execute("SELECT name FROM subs WHERE bot='{}'".format(target))
        results = []
        results = [name[0] for name in cursor]
        cursor.close()
        connection.close()
        return results
    except Exception:
        return []


def add_sub(name, target):
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = "INSERT INTO subs (name, bot) VALUES ('{}', '{}')"\
        .format(name, target)
    result = cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


def delete_sub(name, target):
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = "DELETE FROM subs WHERE name='{}' and bot='{}'".format(name, target)
    result = cursor.execute(sql)
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


def get_subscribers_list(target):
    with app:
        new = []
        for member in app.iter_chat_members(target):
            new.append(name(member.user))
        return new
    raise Exception("Something went wrong")
