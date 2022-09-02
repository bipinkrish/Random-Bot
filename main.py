import telebot
import os
import requests
import json
import time

TOKEN = os.environ.get("TOKEN", "")
CHAT = os.environ.get("CHATID", "")
bot = telebot.TeleBot(TOKEN)


headersList = {
 "authority": "pr0gramm.com",
 "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
 "accept-language": "en-US,en;q=0.9",
 "cache-control": "no-cache",
 "dnt": "1",
 "pragma": "no-cache",
 "referer": "https://pr0gramm.com/",
 "sec-ch-ua-mobile": "?0",
 "sec-ch-ua-platform": "Linux",
 "sec-fetch-dest": "document",
 "sec-fetch-mode": "navigate",
 "sec-fetch-site": "same-origin",
 "sec-fetch-user": "?1",
 "upgrade-insecure-requests": "1",
 "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
            }


def checkvalidid(id):
    resp = requests.get(f"https://pr0gramm.com/api/items/get?id={id}", headers=headersList).json()
    try:
        if resp["error"] == "notFound":
            return 0
        else:
            return 1
    except:
        return 1


def getlatestid():
    resp = requests.get("https://pr0gramm.com/api/items/get", headers=headersList).json()
    newid = resp["items"][0]["id"]
    return newid


def getfile(id):
    maintxt = "https://img.pr0gramm.com/"
    resp = requests.get(f"https://pr0gramm.com/api/items/get?id={id}", headers=headersList).json()
    try:
        imgname = resp["items"][0]["image"]
    except:
        return None,None
    url = maintxt + imgname
    filename = url.split("/")[-1]
    result = requests.get(url)
    return result.content, filename


def main():
    id = getlatestid()
    while(1):
        content,file = getfile(id)

        if file != None:
            print(id)
            with open(file,"wb") as temp:
                temp.write(content)
            if ".jpg" in file or ".png" in file:
                bot.send_photo(CHAT,open(file,"rb"))
            else:
                bot.send_video(CHAT,open(file,"rb"))
            os.remove(file)    

        time.sleep(10)
        id = str(int(id)+1)
        while not checkvalidid(id):
            time.sleep(10)


# polling
bot.infinity_polling(main())