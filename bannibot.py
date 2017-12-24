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
   
    def send_sticker(self, sticker_id, chat_id):
        url = self.api_url + 'sendSticker'
        url += '?chat_id={}'.format(chat_id)
        url += '&sticker={}'.format(sticker_id)
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
   
    def is_sticker(self, update):
        res = True
        try:
            temp = update['message']['sticker']
        except KeyError as err:
            res = False
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
    group_perm = True
    greetings = ('hello', 'hi', 'greetings', 'ciao')
    wished = []

    next_update_id = None
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

                chat = update["message"]["chat"]["id"]
                name = banni.get_name(update)
              
                if now.day == 25 and now.month == 12:
                    if not (name in wished):
                        wished.append(name)
                        send_text = 'Felice Natale ' + name + '!'
                        banni.send_message(send_text, chat)
                        if not (chat in wished):
                            wished.append(chat)
                            send_text_2 = 'https://www.youtube.com/watch?v=3nx7_G5R0oA'
                            banni.send_message(send_text_2, chat)
                        banni.send_sticker('CAADAgAD0QUAAvoLtgjYyEx1T51U2wI', chat)
                        # do this only and do it once
                        continue
                
                # greetings
                if not banni.is_sticker(update):
                    text = update['message']['text']
                    if any([greet in text.lower() for greet in greetings]):
                        if today == now.day and 6 <= hour < 9:
                            send_text = '{} il buongiorno si vede dal mattino'.format(name)
                            #today += 1
                        elif today == now.day and 12 <= hour < 17:
                            send_text = 'Buon pomeriggio bello'.format(name)
                            #today += 1
                        elif today == now.day and 18 <= hour < 23:
                            send_text = 'Buonasera caro {}'.format(name)
                            #today += 1
                        # else:
                            # echo last message
                            # send_text = text
                        if (not update["message"]["chat"]["type"]=="group") or group_perm:
                            banni.send_message(send_text, chat)
                    
                    if 'birra' in text.lower():
                        banni.send_message('Chi invita Angelona?', chat)
                        banni.send_sticker('CAADAgADhQADOQ-GAyBWCYCoan7eAg', chat)

        # before looking for the next update
        time.sleep(0.5)


if __name__ == '__main__':
    main()
