import time
import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('token')

id_channel = '@id_channel'

last_processed_news = ''

@bot.message_handler(content_types=['text'])
def commands (message):
    global last_processed_news 
    if message.text == "Start":
        while True :
            post_text = paresr()

            if post_text is not None and post_text!=last_processed_news:
                bot.send_message( id_channel, post_text, disable_web_page_preview=True)
                last_processed_news = post_text

            time.sleep(300)
    else:
        bot.send_message(message.from_user.id, "Write Start")

def paresr ():
    URL = "https://dev.to/latest"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("div",class_= "crayons-story__body")

    if post :
         title = post .find ("h2", class_ = "crayons-story__title").text.strip()
         return f"{title}\n link : {''}"
    return None

bot.polling()
