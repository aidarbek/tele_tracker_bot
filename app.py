# coding=utf-8
from pyrogram import Client
import time
from utils import *
import sys, traceback

def main():
    app = Client(get_bot_name(), bot_token=get_token())

    def member_in(member, member_list):
        for m in member_list:
            if member == m[0]:
                return True
        return False

    def load(target):
        try:
            return get_subs(target)
        except Exception:
            return []
    def tag_user(name):
        # Add @ to user's username
        try:
            end_found = False
            start = -1
            for i in range(len(name), 0, -1):
                j = i - 1;
                if name[j] == ")":
                    end_found = True
                if name[j] == "(" and end_found:
                    start = j
                    break
            if start >= 0:
                return name[:start+1] + "@" + name[start+1:]
            else:
                return name
        except:
            return name


    with app:
        while True:
            track = get_tracking_channels()
            print(track)
            for pair in track:
                try:
                    owner_name = pair[0]
                    target = pair[1]
                    new = []
                    prev = load(target)
                    new = get_all_subscribers_list(target)
                    if len(prev) == 0:
                        prev = new
                        for uuid, name in prev:
                            print(uuid)
                            add_sub(name, target, uuid)
                    else:
                        sub_count = len(new)
                        for uuid, name in new:
                            if not member_in(uuid, prev):
                                sub_message = "[@{}] ✅ {} subscribed."\
                                    .format(target, tag_user(name))
                                add_sub(name, target, uuid)
                                app.send_message(owner_name, sub_message)
                        for uuid, name in prev:
                            if not member_in(uuid, new):
                                unsub_message = "[@{}] ❌ {} unsubscribed."\
                                    .format(target, tag_user(name), sub_count)
                                delete_sub(uuid, target)
                                app.send_message(owner_name, unsub_message)
                except Exception as err:
                    print(err)
                    traceback.print_exc(file=sys.stdout)
                    time.sleep(60)
                    continue

            time.sleep(5)

if __name__ == '__main__':
    main()
