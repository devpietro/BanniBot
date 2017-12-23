import json
import requests
import time
import urllib.parse
import datetime

TOKEN = "421565171:AAGLyYYO0gX3bHeaBhszF3KP53T1ys4Tk6s"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class Bot:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        url = self.api_url + "getUpdates"
        url += "?timeout={}".format(timeout)
        if offset:
            url += "&offset={}".format(offset)
        #print(url)
        # get url
        resp = requests.get(url)
        # get json from url
        content = resp.content.decode("utf8")
        js = json.loads(content)
        # res = resp.json()["result"]
        return js

    def send_message(self, text, chat_id):
        #params = {'chat_id': chat_id, 'text': text}
        #method = 'sendMessage'
        #resp = requests.post(self.api_url + method, params)
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        resp = requests.post(url)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()        
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return last_update

    def get_name(self, update):
        if update["message"]["chat"]["type"]=="group":
            name = update["message"]['from']['first_name']
            # NB 'language_code' and 'last_name' are also sometimes
            # arguments under ['from'] but not always
        else:
            name = update["message"]["chat"]['first_name']
        return name
        
    def is_fedro(self, update):
        res = False        
        if update['message']['chat']['type']=='group':
            if update['message']['chat']['title']=='Il mito di Fedro':
                res = True
        return res
                
def get_next_update_id(updates):
    num = len(updates['result'])
    if num == 0:
        next_up = None
    else: 
        next_up = int(updates["result"][num-1]["update_id"]) + 1
#    update_ids = []
#    for update in updates["result"]:
#        update_ids.append(int(update["update_id"]))
#    if len(update_ids)==0:
#        last = 0
#    else:
#        last = max(update_ids)
    return next_up

def main():
    next_update_id = None
    greetings = ('hello', 'hi', 'greetings', 'sup', 'ciao')
    banni = Bot(TOKEN)
    #reset updates received while not online
    updates = banni.get_updates(next_update_id)
    next_update_id = get_next_update_id(updates)

    while True:
        now = datetime.datetime.now()
        today = now.day
        hour = now.hour
        updates = banni.get_updates(next_update_id)

        if len(updates["result"]) > 0:
            next_update_id = get_next_update_id(updates)

            for update in updates["result"]:
                try:
                    text = update["message"]["text"]
                except KeyError as err:
                    # temp: handling sticker exception
                    print(err)
                else:
                    chat = update["message"]["chat"]["id"]
                    name = banni.get_name(update)
                    
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
                        # echo last message
                        send_text = text
                banni.send_message(send_text, chat)

        time.sleep(0.5)


if __name__ == '__main__':
    main()
