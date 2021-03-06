#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# creare il bot su @botfather e prendere il token
# collegare la url (webhook) su cui gira al bot attraverso la api:
# https://api.telegram.org/bot399694218:AAErsV9BZ3Oev3J334AL66jPX80MMWF1--Q/setWebhook?url=https://2d79d6cb.ngrok.io
# per far parlare il bot si possono anche usare le direttive API secche:
#
# installare sul sistema ffmpeg: apt install ffmpeg
# installare googletrans: pip3.7 install googletrans==3.1.0a0
#
# API:
# pesci: https://www.fishwatch.gov/api/species

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler,  CallbackQueryHandler)

import logging
import random
import re
import emoji
import json
import requests
from pprint import pprint
from urllib.request import urlopen
import datetime, time

# per farlo parlare
from gtts import gTTS
from pydub import AudioSegment
import subprocess

# from lib import asciigen
# asciigen.from_filename('./python-logo.png', width=40, contrast=1.8)
from googletrans import Translator

# gestione errori
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def _error(update, context):
    logger.warning('Update "%s" caused error "%s"' % (update, context.error))

# funzione dei bitcoin
def getBitcoinPrice():
    URL = "https://www.bitstamp.net/api/ticker/"
    try:
        r = requests.get(URL)
        priceFloat = json.loads(r.text)["last"]
        return round(float(priceFloat), 2)
    except requests.ConnectionError:
        logger.warning("Bitstamp API non va")
        return ''

#funzione per generare audio
def generaAudio(text):
    tts = gTTS(text=text, lang='it')
    source_path_audio = "audio/parola_del_barto.mp3"
    tts.save(source_path_audio)
    mp3_audio = AudioSegment.from_file(source_path_audio, format="mp3")
    destination_path_audio = "audio/parola_del_barto.ogg"
    mp3_audio.export(destination_path_audio, format="opus")
    return destination_path_audio

#generatore di meme random
def generaGif():
    URL = "https://api.giphy.com/v1/gifs/random?api_key=eWHGefzeudCFbj6Fro7pY85SPUsBWakT"
    try:
        r = requests.get(URL)
        data = json.loads(r.text)["data"]
        return data["images"]["original"]["mp4"]
    except requests.ConnectionError:
        logger.warning("Reddit API non va")
        return ''

#generatore di meme random
def generaMeme():
    URL = "https://meme-api.herokuapp.com/gimme/italianmemes"
    try:
        r = requests.get(URL)
        imgUrl = json.loads(r.text)["preview"][-1]
        return imgUrl
    except requests.ConnectionError:
        logger.warning("Reddit API non va")
        return ''

# immagine nasa del giorno
def nasaOfTheDay():
    URL = "https://www.fishwatch.gov/api/species"
    try:
        r = requests.get(URL)
        result = json.loads(r.text)

        translator = Translator()
        translated = translator.translate(result["explanation"], src='en', dest='it')
        result["explanation"] = translated.text
        translated = translator.translate(result["title"], src='en', dest='it')
        result["title"] = translated.text
        return result
    except requests.ConnectionError:
        logger.warning("Reddit API non va")
        return ''

def infoPesce():
    URL = "https://www.fishwatch.gov/api/species"
    try:
        r = requests.get(URL)
        results = json.loads(r.text)
        result = random.choice(results)
        # re.sub('<[^<]+?>', '', text) # strip html
        fish = {}
        result_fish = {}
        fish["Habitat"] = re.sub('<[^<]+?>', '', result["Habitat"])
        fish["Habitat Impacts"] = re.sub('<[^<]+?>', '', result["Habitat Impacts"])
        fish["Species Name"] = re.sub('<[^<]+?>', '', result["Species Name"])
        fish["Fishing Rate"] = re.sub('<[^<]+?>', '', result["Fishing Rate"])
        fish["Physical Description"] = re.sub('<[^<]+?>', '', result["Physical Description"])
        fish["Biology"] = re.sub('<[^<]+?>', '', result["Biology"])
        fish["Taste"] = re.sub('<[^<]+?>', '', result["Taste"])
        translator = Translator()
        # translated_fishs = translator.translate(fish, src='en', dest='it')
        result_fish["Habitat"] = translator.translate(re.sub('\\.n', '\\n', fish["Habitat"]), src='en', dest='it')
        result_fish["Habitat Impacts"] = translator.translate(re.sub('\\.n', '\\n', fish["Habitat Impacts"]), src='en', dest='it')
        result_fish["Species Name"] = translator.translate(re.sub('\\.n', '\\n', fish["Species Name"]), src='en', dest='it')
        result_fish["Fishing Rate"] = translator.translate(re.sub('\\.n', '\\n', fish["Fishing Rate"]), src='en', dest='it')
        result_fish["Physical Description"] = translator.translate(re.sub('\\.n', '\\n', fish["Physical Description"]), src='en', dest='it')
        result_fish["Biology"] = translator.translate(re.sub('\\.n', '\\n', fish["Biology"]), src='en', dest='it')
        result_fish["Taste"] = translator.translate(re.sub('\\.n', '\\n', fish["Taste"]), src='en', dest='it')
        result_fish["url"] = result["Species Illustration Photo"]["src"]
        return result_fish
    except requests.ConnectionError:
        logger.warning("Reddit API non va")
        return ''

def quoteTrump():
    URL = "https://www.tronalddump.io/random/quote"
    try:
        r = requests.get(URL)
        quote = json.loads(r.text)["value"]
    except requests.ConnectionError:
        logger.warning("Tronalddump non va")
        return ''
    translator = Translator()
    translated = translator.translate(quote, src='en', dest='it')
    return translated.text

# Update "
# {'update_id': 323232463,
# 'callback_query':
#    {
#       'from': {'first_name': u'Cosimo', 'is_bot': False, 'id': 132109820, 'language_code': u'it-IT'},
#       'chat_instance': u'-5015160140212802456',
#       'message': {
#                   'delete_chat_photo': False, 'new_chat_photo': [],
#                   'from': {'username': u'AvvBartoBot', 'first_name': u'AvvocatoBartolini', 'is_bot': True, 'id': 399694218},
#                   'text': u'Use inline keyboard', 'entities': [], 'channel_chat_created': False, 'new_chat_members': [], 'supergroup_chat_created': False,
#                   'chat': {'first_name': u'Cosimo', 'type': u'private', 'id': 132109820},
#                   'photo': [], 'date': 1506428888, 'group_chat_created': False, 'message_id': 301, 'new_chat_member': None
#                   },
#       'data': u'ip',
#       'id': u'567407356608626168'
#    }
# }"
#

# Gestione del menu
commands_list = "/barto\n/info\n/status\n/macron\n/vincosicuro\n/fantasia\n/shrek\n/scandalo\n/sigla\n/bitcoin\n/fish\n/nasa\n/gif\n/meme\n/trump\n/parla"
def callbacks(update, context):
    if update.callback_query.data == "inline":
        print(update)
	#print('Callback Query:', update.message.query_id, update.message.chat_id, update.message.query_data)
    if update.callback_query.data == 'ip':
        my_ip = urlopen('http://ip.42.pl/raw').read()
        #context.bot.editMessageText(inline_message_id=update.callback_query.inline_message_id, text="Do you want to turn On or Off light? Light is ON")
        context.bot.answer_callback_query(update.callback_query.id, text=my_ip)
        #context.bot.sendMessage(chat_id=update.message.chat_id, text=my_ip)
    elif update.callback_query.data == 'info':
        # info=json.dumps(context.bot.getUpdates(),sort_keys=True, indent=4)
        context.bot.answer_callback_query(update.callback_query.id, text=update.callback_query.message.chat.id)
    elif update.callback_query.data == 'bitcoin':
        context.bot.sendMessage(chat_id=update.callback_query.message.chat.id, text='In questo momento 1 bitcoin vale $%f' % round(getBitcoinPrice(),2))
        context.bot.answer_callback_query(update.callback_query.id, text='In questo momento 1 bitcoin vale $%d' % getBitcoinPrice())
    elif update.callback_query.data == 'parla':
        sparajingle_audio(update.callback_query, context)
    elif update.callback_query.data == 'gif':
        inviagif(update.callback_query, context)
    elif update.callback_query.data == 'meme':
        send_meme(update.callback_query, context)
    elif update.callback_query.data == 'trump':
        citazionetrump(update.callback_query, context)
    elif update.callback_query.data == 'nasa':
        fotonasa(update.callback_query, context)
    elif update.callback_query.data == 'time':
        ts = time.time()
        context.bot.answer_callback_query(update.callback_query.id, text=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S'))
    elif update.callback_query.data == 'credits':
        context.bot.sendMessage(chat_id=update.callback_query.message.chat.id, text='Cosimo Zecchi mio padrone e creatore. Per donazioni in btc: 3JDyBLvw3nRx54jesn9chtnRJpG7Ftc4o7')
        context.bot.answer_callback_query(update.callback_query.id, text='Cosimo Zecchi mio padrone e creatore. Per donazioni in btc: 3JDyBLvw3nRx54jesn9chtnRJpG7Ftc4o7')
    elif update.callback_query.data == 'help':
        context.bot.sendMessage(chat_id=update.callback_query.message.chat.id, text=commands_list)

def chatinfo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id )

def status(update, context):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text='Bitcoin', callback_data='bitcoin'),],
                         [InlineKeyboardButton(text='Parla', callback_data='parla'),],
                         [InlineKeyboardButton(text='Gif', callback_data='gif'), InlineKeyboardButton(text='Meme', callback_data='meme')],
                         [InlineKeyboardButton(text='Trump', callback_data='trump'), InlineKeyboardButton(text='Nasa', callback_data='nasa')],
                         [InlineKeyboardButton(text='IP', callback_data='ip'), InlineKeyboardButton(text='Info', callback_data='info')],
                         [InlineKeyboardButton(text='Time', callback_data='time'), InlineKeyboardButton(text='Credits', callback_data='credits')],
                         [InlineKeyboardButton(text='Help', callback_data='help'),],
                     ])
    context.bot.send_message(chat_id=update.message.chat_id, text='BartoBot v1.0 \nSono qui per servivi (col cazzo,sai!):')
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text='Scegli il comando', reply_markup=keyboard)
    # r = types.InlineQueryResultArticle(
    #     id="1",
    #     title="Title",
    #     input_message_content=types.InputTextMessageContent(message_text="Test"),
    #     reply_markup=keyboard
    # )
    # context.bot.answer_inline_query(update.message.chat_id, r)
# fine gestione del menu

def sigla(update, context):
    context.bot.send_audio(chat_id=update.message.chat_id, audio=open('sounds/neverending.mp3', 'rb'))

def sendImage(update, context, imagename):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('images/'+imagename+'.jpg', 'rb'))

def macron(update, context):
    sendImage(update, context, 'macron')
def fantasia(update, context):
    sendImage(update, context, 'fantasia')
def macron(update, context):
    sendImage(update, context, 'macron')
def shrek(update, context):
    sendImage(update, context, 'shrek')
def vincosicuro(update, context):
    sendImage(update, context, 'vincosicuro')
def scandalo(update, context):
    sendImage(update, context, 'praga')
def attilio(update, context):
    sendImage(update, context, 'attilio')
    context.bot.send_message(chat_id=update.message.chat_id, text='Io voto Italia nel cuore. Viva Attilio!')


# ripete quello che viene scritto
def echo(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

# audio messages
def sparajingle_audio(update, context):
    set_frasi = ragione + no_ragione + frasi_tipiche + offese + frasi_fia
    path_audio = generaAudio(random.choice(set_frasi).format(getNomecumpa(update.message.from_user.first_name)))
    context.bot.send_voice(chat_id=update.message.chat_id, voice=open(path_audio, 'rb'))

# pesce random
def scheda_pesce(update, context):
    fish = infoPesce()
    context.bot.send_message(chat_id=update.message.chat_id, text="Conoscete il %s ?" % fish["Species Name"].text)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=fish["url"], caption=fish["Species Name"].text)
    context.bot.send_message(chat_id=update.message.chat_id, text="Bello vero?")
    context.bot.send_message(chat_id=update.message.chat_id, text=fish["Physical Description"].text)
    context.bot.send_message(chat_id=update.message.chat_id, text=fish["Biology"].text)
    context.bot.send_message(chat_id=update.message.chat_id, text="A questo punto vi starete chiedendo dove vivono e come pescarli")
    context.bot.send_message(chat_id=update.message.chat_id, text=fish["Habitat"].text)
    context.bot.send_message(chat_id=update.message.chat_id, text=fish["Habitat Impacts"].text)
    context.bot.send_message(chat_id=update.message.chat_id, text=fish["Fishing Rate"].text)
    context.bot.send_message(chat_id=update.message.chat_id, text="Se vi interessa mangiarlo sappiate che:")
    context.bot.send_message(chat_id=update.message.chat_id, text=fish["Taste"].text)

# send meme
def send_meme(update, context):
    context.bot.sendPhoto( update.message.chat_id, generaMeme() )

def cops(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_cops))

def colzi(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text='Colzi, amico fedele!')

def anita(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text='Scarlo, se vendi la lotus non sono piu tuo amico')

def rosalba(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text='Zek sei cambiato')

def rosaria(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text='Tutti a o\'paesiello, ue ue!')

def citazionetrump(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Trump una volta ha detto: %s' % quoteTrump() )

def bitcoinvalue(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='In questo momento 1 bitcoin vale $%d' % getBitcoinPrice() )

def fotonasa(update, context):
    nasa = nasaOfTheDay()
    context.bot.send_photo(chat_id=update.message.chat_id, photo=nasa["url"], caption=nasa["title"])
    context.bot.send_message(chat_id=update.message.chat_id, text=nasa["explanation"])

def inviagif(update, context):
    context.bot.send_video(chat_id=update.message.chat_id, video=generaGif())
    context.bot.send_message(chat_id=update.message.chat_id, text="ahahaha")

# sistema per creare una grammatica
# s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
# p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
# s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]
# p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
# infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]
#
# def sing_sen_maker():
#     '''Makes a random senctence from the different parts of speech. Uses a SINGULAR subject'''
#     if input("Would you like to add a new word?").lower() == "yes":
#         new_word = input("Please enter a singular noun.")
#         s_nouns.append(new_word)
#     else:
#     	print random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)

# i dizionari del barto
# frasi tipiche raccolte tutte insieme
frasi_tipiche = ["Vinco sicuro!", "Caaaaaaazzz estremo!", "Sono il numero 1", "Puppatemelo sai", "Mi depilo le palle", "Oggettivamente", "Mmmm che schifo!", "Milan campione!", "Poeri poeri", "MANGIARE!", "Te lo metto nel culo!", "Indubbiamente!", "Sorto dopo cena", "Che poverta!",
                "Se non duro due ore ti do 3000 euro", "Ue ciccia, sei bellissima", "O\' paesiello, ue ue", "Piazzami sta fia", "L\'ho giocato alla snai", "Comprate i bitcoin", "Devo comprare la McLaren", "Col cazzo, sai!", "Che fica anale", "Ti trombo nel culo!","Quest\'estate vo a Viareggio sai! M\'importa una sega",
                "Raga non insegnate al babbo a trombare", "Siete dei babbazzi!", "Trombare bere mangiare pescare guidare" ]

#frasi per dare ragione
ragione = [ "Giusto!", "Anale!", "Certo {}", "Ovviamente {}", "{}, siamo i numeri uno", "Bravo {}", "Caaaaaaazzz estremo!", "{}, penso che presto saro ricco" ]
no_ragione = [ "Bravo coglione", "Ti sbagli di grosso", "Che cazzo dici", "Poveraccio", "{}, guarda non commento"]
#frasi per offendere
offese = ["Non mi tritate la minchia", "Poero {}", "Col cazzo sai!", "Puppatemelo sai", "{}, puppamelo!", "Cazzo vuoi?", "{}, ora hai proprio rotto il cazzo", "{} sei un babbazzo!", "Siete dei babbazzi!", "{} guarda non commento"]
#frasi per salutare in partenza
saluti_partenza = ["Ciao, ora devo andare a trombare", "Ciao, ora devo andare a guadagnare", "Ora vado in palestra. Ciao!" ]
frasi_buongiorno = [ "Buongiorno a te {}", "{}, grazie","Grazie, ora andiamo a fare soldi", "grazie {}, stai bene?", "{}, son gia in ufficio, che poverta" ]
frasi_bitcoin = ["Comprate i bitcoin, poi mi ringrazierete", "{}, non vendere assolutamente i bitcoin!", "{}, penso che presto saro ricco" ]
frasi_lucia = ["Fo passare Natale e il compleanno, cosi mi fa il regalo, poi la mollo", "Ufficialmente io sono rimasto a casa, niente tag su FB", "Appena c\'ha le sue cose la lascio", "Raga ho avuto un sogno e mi sono svegliato urlando. Al prossimo mestruo la lascio" ]
frasi_roby2 = ["Che fia imperiale", "Il mese prossimo ci mettiamo insieme", "{}, una fia del genere te la scordi", "Stasera se ci si vede non postate foto", "{} stasera posso venire a trombarla da te? Non ha ancora pronta la casa"]
frasi_cena_barto = ["Mangiare {}! MANGIARE!!!", "{}, imbuzzarsi!!", "Cibo!", "Ma quanto mangi {}?", "Mmmm che schifo!" ]
frasi_cena_generiche = [ "MANGIARE!", "Mangiare. MANGIAREEEE!!!!", "Imbuzzarsi!!", "Cibo!", "Ma quanto mangiate?", "MANGIARE!" ]
frasi_pesca = ["FISH!!!!", "Da vero maschio alpha" ]
frasi_macchine = ["Domenica ho il raduno", "Devo comprare la McLaren", "Ho una ferrari per le mani", "Se piazzo la ferrari faccio tanti soldi", "Devo cambiare gli ammortizzatori", "Non e\' tanto comprarla. La botta e\' sull\'assicurazione furto incendio atti vandalici e mini kasko, almeno 3500 euro annui" ]
frasi_fia = [ "Anale!", "Raga, non insegnate al babbo a trombare", "Che puttana!", "Ue ciccia, sei bellissima", "Che fica anale!", "Che fica stratosferica", "{}, piazzami sta fia", "La trombo nel culo", "Che delizia assoluta" ]
frasi_milan = ["Milan campione", "Ritorneremo!", "La gioco alla snai", "Si gioca contro le merde?", "Si vince sicuro" ]
frasi_moralizzatori = [ "{} mi hai rotto il cazzo. Faccio come mi pare", "{} il moralizzatore","Sono arrivati i moralizzatori", "Fatevi i cazzi vostri",
            "Si esco con due ragazze e allora? chi non le ha oggigiorno", "Da vero maschio alpha", "{} guarda ormai dal punto di vista sentimentale vivo alla giornata e faccio cio che mi va" ]
frasi_cops = [ "Poero Cops!", "Non esagerate, cops e\' molto sensibile", "Poero Cops!", "Poero Cops!" ]
frasi_stare_bene = [ "Bene", "Io sto benissimo", "Benissimo, {}", "{}, sto molto bene" ]
frasi_tie = [ "Bene sai!", "Tie!", "Godo!"]
frasi_ridere = [ "Cazzo ridi?", "{}, cazzo ridi?", "Ah ah ah. Che ridere", "Sono contento vi faccia ridere", "ahahaha", "Bella questa"]
frasi_palle = ["Siete sempre piu pelosi fate schifo!", "Vi ricordo che quando ve lo puppano gli rimane i peli tra i denti a me invece leccano anche sopra il cazzo dove voi avete i peli ed è una bella sensazione che voi non conoscerete mai babbazzi"]
frasi_politica = [ "L\'Italia e\' allo sbando ed e\' tutta colpa del PD! Merdosi!", "Musulmani di merda!", "Comunisti maledetti!", "Vota Fratelli d\'Italia!" ]
frasi_segreto = ["{}, non lo dire a nessuno", "Oh {}, resta tra noi. Non lo dire a nessuno"]
# traduzioni nomi
nomi_cumpa = {'Cosimo': 'Zek', 'David': 'Mazza', 'Lorenzo': 'Cops', 'Fabrizio': 'Sancio', 'Simone': 'Scarlo', 'Alex': 'Coglionazzo', 'L': 'Paoli', 'Francesco': 'Ciccio', 'Marco': 'Salva', 'Sandro': 'Sandrino'}

def getNomecumpa(nome):
    if nome in nomi_cumpa:
        return nomi_cumpa[nome]
    else:
        return nome
def saluta(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Ciao %s, io sto molto bene!" % getNomecumpa(update.message.from_user.first_name) )

def buongiorno(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_buongiorno).format(getNomecumpa(update.message.from_user.first_name)) )

def stobene(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_stare_bene).format(getNomecumpa(update.message.from_user.first_name)) )

def tie(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_tie).format(getNomecumpa(update.message.from_user.first_name)) )

def palle(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_palle).format(getNomecumpa(update.message.from_user.first_name)) )

def politica(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_politica).format(getNomecumpa(update.message.from_user.first_name)) )

def sparajingle(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_tipiche).format(getNomecumpa(update.message.from_user.first_name)))

def offendi(update, context):
    offesa = random.choice(offese)
    context.bot.send_message(chat_id=update.message.chat_id, text=offesa.format(getNomecumpa(update.message.from_user.first_name)) )

def dare_ragione(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(ragione).format(getNomecumpa(update.message.from_user.first_name)) )

def bitcoin(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_bitcoin).format(getNomecumpa(update.message.from_user.first_name)))

def cibo(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_cena_generiche).format(getNomecumpa(update.message.from_user.first_name)))

def ridere(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_ridere).format(getNomecumpa(update.message.from_user.first_name)))

def auto(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_macchine).format(getNomecumpa(update.message.from_user.first_name)))

def calcio(update, context):
     if re.match("^(.*)[jJ]uve(.*)$", update.message.text):
         context.bot.send_message(chat_id=update.message.chat_id, text="Merde!")
     else:
         context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_milan).format(getNomecumpa(update.message.from_user.first_name)))

def pesca(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_pesca).format(getNomecumpa(update.message.from_user.first_name)))

def poero(update, context):
     if update.message.from_user.first_name == "Alessandro" or update.message.from_user.first_name == "Alex":
         poero_match = re.match(r"^.*[Pp]oero (.*)$", update.message.text, re.M|re.I)
         if poero_match:
             passcontext.bot.send_message(chat_id=update.message.chat_id, text='Davvero, {} e\' proprio un babbazzo.'.format(poero_match.group(1)))
         else:
             passcontext.bot.send_message(chat_id=update.message.chat_id, text='Hai ragione Barto')
     else:
         passcontext.bot.send_message(chat_id=update.message.chat_id, text='Mamma mia che babbazzo')

def fica(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_fia).format(getNomecumpa(update.message.from_user.first_name)))

def moralizzatori(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_moralizzatori).format(getNomecumpa(update.message.from_user.first_name)))

def lucy(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_lucia).format(getNomecumpa(update.message.from_user.first_name)))

def roby2(update, context):
     context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_roby2).format(getNomecumpa(update.message.from_user.first_name)))

def arrivederci(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(saluti_partenza).format(getNomecumpa(update.message.from_user.first_name)) )
# quando le frasi contengono il nome del barto lui sceglie quale frase usare
# TODO: inserire una variabile per gestire i cambi di umore
def invocazione(update, context):
    # saluta
    cumpa_match = re.match(r"^.*([Zz]ek|[Ss]ancio|[Ss]carlo|[Mm]azza|[Cc]ops|[Cc]iccio|[Pp]aoli).*$", update.message.text, re.M|re.I)
    if re.match("^.*[Cc]iao.*$", update.message.text):
        saluta(update, context)
    elif re.match("^.*[Gg]razie.*$", update.message.text):
        context.bot.send_message(chat_id=update.message.chat_id, text="Prego {}".format(getNomecumpa(update.message.from_user.first_name)))
    elif re.match("^.*( u[Eeèé] |U[Eeèé] ).*$", update.message.text):
        saluta(update, context)
    elif re.match("^.*[Bb]uongiorn.*$", update.message.text):
        buongiorno(update, context)
    elif re.match("^(.*)[Cc]ome stai(.*)$", update.message.text):
        context.bot.send_message(chat_id=update.message.chat_id, text="%s, sto molto bene" % getNomecumpa(update.message.from_user.first_name) )
    elif re.match("^.*(cib|mangi| cena |ristorante|pranz|pizza|bistecca|aragosta|ostriche).*$", update.message.text):
        context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_cena_barto).format(getNomecumpa(update.message.from_user.first_name)))
    elif cumpa_match:
        offendi_match = re.match("^.*([Oo]ffendi|[Ii]nsulta|qualcosa a) .*$", cumpa_match.group())
        if offendi_match:
                nome = getNomecumpa(update.message.from_user.first_name)
                offese.append('No ' + nome + ', ' + cumpa_match.group(1) + ' e\' un amico fedele.')
                context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(offese).format(cumpa_match.group(1), getNomecumpa(update.message.from_user.first_name)) )
        else:
                ragione_mix = [ "{0}, ha ragione {1}.", "{1}, ha ragione {0}."]
                context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(ragione_mix).format(cumpa_match.group(1), getNomecumpa(update.message.from_user.first_name)) )
    elif re.match("^.*[Cc]oglione.*$", update.message.text) or re.match("^.*[Ss]tupido.*$", update.message.text) or re.match("^(.*)[Ff]ava(.*)$", update.message.text) or re.match("^(.*)[Ss]cemo(.*)$", update.message.text):
        offendi(update, context)
    elif re.match("^.*[Gg]rand.*$", update.message.text) or re.match("^(.*)[Mm]mitico(.*)$", update.message.text) or re.match("^(.*)[Bb]rav(.*)$", update.message.text):
        dare_ragione(update, context)
    elif re.match("^.*[Pp]ens.*$", update.message.text) or re.match("^.*[Dd]ico bene.*$", update.message.text) or re.match("^(.*)[Dd]ici (.*)$", update.message.text) or re.match("^(.*)[Vv]ero (.*)$", update.message.text) or re.match("^(.*)[Gg]iusto (.*)$", update.message.text):
        ragione_no_ragione = ragione + no_ragione
        context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(ragione_no_ragione).format(getNomecumpa(update.message.from_user.first_name)) )
    elif re.match("^.*([Aa] presto|[Aa]rrivederci| a dopo).*$", update.message.text):
        arrivederci(update, context)
    else:
        offendi(update, context)

def segreto(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_segreto).format(getNomecumpa(update.message.from_user.first_name)) )

def help_list(update, context):
    context.bot.sendMessage(chat_id=update.message.chat.id, text=commands_list)

updater = Updater(token='399694218:AAErsV9BZ3Oev3J334AL66jPX80MMWF1--Q', use_context=True)
dispatcher = updater.dispatcher
# imposta i comandi
start_handler = CommandHandler('saluta', saluta)
dispatcher.add_handler(start_handler)
dispatcher.add_handler( CommandHandler('barto', sparajingle) )
dispatcher.add_handler( CommandHandler('info', chatinfo) )
dispatcher.add_handler( CommandHandler('status', status) )
dispatcher.add_handler( CommandHandler('macron', macron) )
dispatcher.add_handler( CommandHandler('vincosicuro', vincosicuro) )
dispatcher.add_handler( CommandHandler('fantasia', fantasia) )
dispatcher.add_handler( CommandHandler('shrek', shrek) )
dispatcher.add_handler( CommandHandler('scandalo', scandalo) )
dispatcher.add_handler( CommandHandler('sigla', sigla) )
dispatcher.add_handler( CommandHandler('bitcoin', bitcoinvalue) )
dispatcher.add_handler( CommandHandler('fish', scheda_pesce) )
dispatcher.add_handler( CommandHandler('nasa', fotonasa) )
dispatcher.add_handler( CommandHandler('gif', inviagif) )
dispatcher.add_handler( CommandHandler('meme', send_meme) )
dispatcher.add_handler( CommandHandler('trump', citazionetrump) )
dispatcher.add_handler( CommandHandler('parla', sparajingle_audio) )
dispatcher.add_handler( CommandHandler('help', help_list) )
# context.bot.send_message(emojize("Barto :moyai:", use_aliases=True))

# intercettori di testo dei messaggi
# vecchia versione
# dispatcher.add_handler(RegexHandler(re.compile(r"^.*(palle|peli|depila).*$"), palle))
# nuova versione
# MessageHandler(Filters.regex('pattern'), callback)

regcops = "^(.*)[Cc]ops(.*)$"
regmoai = "^(.*)" + emoji.emojize(':moyai:', use_aliases=True) + "(.*)$"
regsegreto = "^.*(segreto|dire.*cosa).*$"
regbitcoinvalue = "^.*([Qq]uanto.*val.*bitcoin).*$"

dispatcher.add_handler(MessageHandler(Filters.regex(regcops), cops))
dispatcher.add_handler(MessageHandler(Filters.regex(regmoai), sparajingle))
dispatcher.add_handler(MessageHandler(Filters.regex(regsegreto), segreto))
dispatcher.add_handler(MessageHandler(Filters.regex(regbitcoinvalue), bitcoinvalue))

dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Bb]arto.*parla).*$"), sparajingle_audio))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Bb]arto.*meme).*$"), send_meme))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Tt]rump).*$"), citazionetrump))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Bb]arto.*foto.*spazio).*$"), fotonasa))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Bb]arto.*gif).*$"), inviagif))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Cc]olzi.*$"), colzi))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Cc]ome state|[Tt]utto bene).*$"), stobene))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*(macchina|lotus|ferrari|mclaren|auto).*$"), auto))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Mm]ilan|calcio|[Jj]uve|[Cc]hampions|[Pp]artita|[Cc]ampionato).*$"), calcio))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*(ragazza).*$"), fica))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*( fia | fica | figa | fia| figa| fica).*$"), fica))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*pesc.*$"), pesca))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Aa]nita.*$"), anita))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Aa]ttilio.*$"), attilio))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Rr]osaria.*$"), rosaria))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Rr]osalba.*$"), rosalba))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Bb]itcoin.*$"), bitcoin))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Pp]oero.*$"), poero))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Ll]ucy.*[Rr]oby.{0,1}2|[Rr]oby.{0,1}2.*[Ll]ucy|[Ll]ucia.*[Rr]oby.{0,1}2|[Rr]oby.{0,1}2.*[Ll]ucia).*$"), moralizzatori))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Ll]ucy.*$"), lucy))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Ll]ucia.*$"), lucy))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*([Rr]oby2|[Rr]oby 2).*$"), roby2))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*foto.*scandalo.*$"), scandalo))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*(voto|politica|Meloni|[Bb]erlusconi|Salvini).*$"), politica))
# dispatcher.add_handler(MessageHandler(Filters.regex("^(.*)[Cc]iao(.*)[Bb]arto(.*)$"), saluta))
# dispatcher.add_handler(MessageHandler(Filters.regex("^(.*)[Pp]ens(.*)[Bb]arto(.*)$"), dare_ragione))
# dispatcher.add_handler(MessageHandler(Filters.regex("^(.*)[Bb]arto(.*)$"), offendi))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*[Bb]arto.*$"), invocazione))
#altrimenti mi intercettano anche se c'è barto
dispatcher.add_handler(MessageHandler(Filters.regex("^.*(cib|mangi| cena |ristorante|pranz|pizza|bistecca|aragosta|ostriche).*$"), cibo))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*(ahah).*$"), ridere))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*(sfiga).*$"), tie))
dispatcher.add_handler(MessageHandler(Filters.regex("^.*(palle|peli|depila).*$"), palle))
# fineintercettori
# intercetta i callback
dispatcher.add_handler( CallbackQueryHandler(callbacks) )

# va aggiunto un nuovo error handler
dispatcher.add_error_handler(_error)
updater.start_polling()
updater.idle()


