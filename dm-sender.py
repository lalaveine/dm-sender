#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

SLEEP_TIME = 30

class main():

    def send_dm():
        cpass = configparser.RawConfigParser()
        cpass.read('config.data')
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        user_phone = cpass['cred']['phone']

        client = TelegramClient(user_phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(user_phone)
            client.sign_in(user_phone, code=input('code :'))
        
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['name'] = row[1]
                user['message'] = row[2]
                users.append(user)
         
        for user in users:
            receiver = client.get_input_entity(user['username'])

            try:
                print("[+] Sending Message to:", user['name'])
                client.send_message(receiver, user['message'])
                print("[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)

            except PeerFloodError:
                print("[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                sys.exit()

            except Exception as e:
                print("[!] Error:", e)
                print("[!] Trying to continue...")
                continue
        client.disconnect()
        print("Done. Message sent to all users.")



if __name__ == "__main__":
    main.send_dm()
