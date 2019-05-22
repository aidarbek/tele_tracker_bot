# coding=utf-8
from pyrogram import Client
import time
from utils import *


def main():
    app = Client(get_bot_name(), bot_token=get_token())

    def member_in(member, member_list):
        for m in member_list:
            if member == m:
                return True
        return False

    def load(target):
        try:
            return get_subs(target)
        except Exception:
            return []

    with app:
        while True:
            track = get_tracking_channels()
            print(track)
            for pair in track:
                owner_name = pair[0]
                target = pair[1]
                new = []
                prev = load(target)
                new = get_subscribers_list(target)
                if len(prev) == 0:
                    prev = new
                    for el in prev:
                        add_sub(el, target)
                    print("Initial list gotten")
                else:
                    for member in new:
                        if not member_in(member, prev):
                            sub_message = "[@{}] {} subscribed"\
                                .format(target, member)
                            #print(sub_message)
                            add_sub(member, target)
                            app.send_message(owner_name, sub_message)
                    for member in prev:
                        if not member_in(member, new):
                            unsub_message = "[@{}] {} unsubscribed"\
                                .format(target, member)
                            #print(unsub_message)
                            delete_sub(member, target)
                            app.send_message(owner_name, unsub_message)
            time.sleep(5)

if __name__ == '__main__':
    main()
