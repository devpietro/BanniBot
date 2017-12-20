import json
import requests
import time
import urllib.parse
import datetime

TOKEN = "421565171:AAGLyYYO0gX3bHeaBhszF3KP53T1ys4Tk6s"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None, timeout=30):
    url = URL + "getUpdates"
    url += "?timeout={}".format(timeout)
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
        except KeyError as err:
            # temp: handling sticker exception
            print(err)
        else:
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def main():
    last_update_id = None
    greetings = ('hello', 'hi', 'greetings', 'sup', 'ciao')
    now = datetime.datetime.now()
    today = now.day
    hour = now.hour
    n = 0
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            #echo_all(updates)

            for update in updates["result"]:
                try:
                    text = update["message"]["text"]
                except KeyError as err:
                    # temp: handling sticker exception
                    print(err)
                else:
                    chat = update["message"]["chat"]["id"]
                    name = update["message"]['chat']['first_name']
                    
                    if text.lower() in greetings and today == now.day and 6 <= hour < 12:
                        send_text = 'Good Morning {}'.format(name)
                        #today += 1

                    elif text.lower() in greetings and today == now.day and 12 <= hour < 17:
                        send_text = 'Good Afternoon {}'.format(name)
                        #today += 1

                    elif text.lower() in greetings and today == now.day and 17 <= hour < 23:
                        send_text = 'Good Evening {}'.format(name)
                        #today += 1#
                    else:
                        send_text = text
                send_message(send_text, chat)

        time.sleep(0.5)


if __name__ == '__main__':
    main()
