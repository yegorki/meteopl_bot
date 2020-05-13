#!/usr/bin python3
from telegram.ext import Updater
import datetime
from urllib.request import Request, urlopen
from bs4 import  BeautifulSoup
import logging
from telegram.ext import CommandHandler
from random import randrange

updater = Updater(token='')
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Share some location to get a weather picture or send /Konigsberg command to see a picture for Kaliningrad.\nHow to read forecast: /legend")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def konigsberg(bot, update):
    '''q = Request("http://m.meteo.pl/search/eu?miastoEU=&wspolrzedneEU=N54%C2%B041%27+E20%C2%B029%27&typeEU=coords&prognozaEU=60&slugEU=")'''
    q = Request("http://m.meteo.pl/row/339/col/241")
    mybytes = urlopen(q).read()
    mystr = mybytes.decode("utf8")
    urlopen(q).close()
    soup = BeautifulSoup(mystr, "html.parser")
    url = soup.find('img', class_='border')['src']
    url = url.replace('=pl','=en')
    bot.send_photo(chat_id=update.message.chat_id, photo=url)
    if randrange(10) == 0:
        bot.send_message(chat_id=update.message.chat_id, text="Try to share any location to get forecast for that place! 📍")


konigsberg_handler = CommandHandler('konigsberg', konigsberg)
dispatcher.add_handler(konigsberg_handler)


def location(bot, update):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    url = "http://www.meteo.pl/um/php/mgram_search.php?NALL=" + str(lat) + "&EALL=" + str(lon) + "&lang=en"
    q = urlopen(url)
    finalurl = q.geturl()
    #print(finalurl)
    row = finalurl[finalurl.index('&row=') + 5:finalurl.index('&col=')]
    col = finalurl[finalurl.index('&col=') + 5:finalurl.index('&lang')]
    lat_deg = str(int(lat))
    lat_min = str(round((int((lat % 1)*60)),2))
    lon_deg = str(int(lon))
    lon_min = str(round((int((lon % 1)*60)),2))
    #q = Request("http://m.meteo.pl/search/eu?miastoEU=&wspolrzedneEU=N"+ lat_deg +"%C2%B0"+ lat_min +"%27+E"+ lon_deg +"%C2%B0"+ lon_min +"%27&typeEU=coords&prognozaEU=60&slugEU=")
    q = Request("http://m.meteo.pl/row/" + str(row) + "/col/" + str(col))
    mybytes = urlopen(q).read()
    mystr = mybytes.decode("utf8")
    urlopen(q).close()
    soup = BeautifulSoup(mystr, "html.parser")
    url = soup.find('img', class_='border')['src']
    url = url.replace('=pl','=en')
    bot.send_photo(chat_id=update.message.chat_id, photo=url)

from telegram.ext import MessageHandler, Filters
location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)


def legend(bot, update):
    url = "https://www.meteo.pl/um/metco/leg_um_en_cbase_256.png"
    bot.send_photo(chat_id=update.message.chat_id, photo=url)

legend_handler = CommandHandler('legend', legend)
dispatcher.add_handler(legend_handler)

updater.start_polling()
