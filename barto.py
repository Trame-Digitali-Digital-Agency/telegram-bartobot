#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# creare il bot su @botfather e prendere il token
# collegare la url (webhook) su cui gira al bot attraverso la api:
# https://api.telegram.org/bot399694218:AAErsV9BZ3Oev3J334AL66jPX80MMWF1--Q/setWebhook?url=https://2d79d6cb.ngrok.io
# per far parlare il bot si possono anche usare le direttive API secche:
#
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
from urllib import urlopen
import datetime, time
# from lib import asciigen
# asciigen.from_filename('./python-logo.png', width=40, contrast=1.8)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# funzione dei bitcoin
def getBitcoinPrice():
    URL = "https://www.bitstamp.net/api/ticker/"
    try:
        r = requests.get(URL)
        priceFloat = json.loads(r.text)["last"]
        return round(float(priceFloat), 2)
    except requests.ConnectionError:
        return "Bitstamp API non va"

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
def callbacks(bot,update):
    if update.callback_query.data == "inline":
        print(update)
	#print('Callback Query:', update.message.query_id, update.message.chat_id, update.message.query_data)
    if update.callback_query.data == 'ip':
        my_ip = urlopen('http://ip.42.pl/raw').read()
        #bot.editMessageText(inline_message_id=update.callback_query.inline_message_id, text="Do you want to turn On or Off light? Light is ON")
        bot.answer_callback_query(update.callback_query.id, text=my_ip)
        #bot.sendMessage(chat_id=update.message.chat_id, text=my_ip)
    elif update.callback_query.data == 'info':
        # info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4)
        bot.answer_callback_query(update.callback_query.id, text=update.callback_query.message.chat.id)
    elif update.callback_query.data == 'bitcoin':
        bot.sendMessage(chat_id=update.callback_query.message.chat.id, text='In questo momento 1 bitcoin vale $%f' % round(getBitcoinPrice(),2))
        bot.answer_callback_query(update.callback_query.id, text='In questo momento 1 bitcoin vale $%d' % getBitcoinPrice())
    elif update.callback_query.data == 'time':
        ts = time.time()
        bot.answer_callback_query(update.callback_query.id, text=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S'))
    elif update.callback_query.data == 'credits':
        bot.sendMessage(chat_id=update.callback_query.message.chat.id, text='Cosimo Zecchi mio padrone e creatore')
        bot.answer_callback_query(update.callback_query.id, text='Cosimo Zecchi mio padrone e creatore')

def chatinfo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id )

def status(bot, update):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text='Bitcoin', callback_data='bitcoin'),],
                         [InlineKeyboardButton(text='IP', callback_data='ip'),
                         InlineKeyboardButton(text='Info', callback_data='info')],
                         [InlineKeyboardButton(text='Time', callback_data='time'),InlineKeyboardButton(text='Credits', callback_data='credits')],
                     ])
    bot.send_message(chat_id=update.message.chat_id, text='BartoBot v0.3 \nSono qui per servivi (col cazzo,sai!):')
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text='Scegli il comando', reply_markup=keyboard)
    # r = types.InlineQueryResultArticle(
    #     id="1",
    #     title="Title",
    #     input_message_content=types.InputTextMessageContent(message_text="Test"),
    #     reply_markup=keyboard
    # )
    # bot.answer_inline_query(update.message.chat_id, r)
# fine gestione del menu

def sigla(bot, update):
    bot.send_audio(chat_id=update.message.chat_id, audio=open('sounds/neverending.mp3', 'rb'))

def sendImage(bot, update, imagename):
    bot.send_photo(chat_id=update.message.chat_id, photo=open('images/'+imagename+'.jpg', 'rb'))

def macron(bot, update):
    sendImage(bot, update, 'macron')
def fantasia(bot, update):
    sendImage(bot, update, 'fantasia')
def macron(bot, update):
    sendImage(bot, update, 'macron')
def shrek(bot, update):
    sendImage(bot, update, 'shrek')
def vincosicuro(bot, update):
    sendImage(bot, update, 'vincosicuro')
def scandalo(bot, update):
    sendImage(bot, update, 'praga')
def attilio(bot, update):
    sendImage(bot, update, 'attilio')
    bot.send_message(chat_id=update.message.chat_id, text='Io voto Italia nel cuore. Viva Attilio!')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

# ripete quello che viene scritto
def echo(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def cops(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_cops))

def colzi(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text='Colzi, amico fedele!')

def anita(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text='Scarlo, se vendi la lotus non sono piu tuo amico')

def rosalba(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text='Zek sei cambiato')

def rosaria(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text='Tutti a o\'paesiello, ue ue!')

def bitcoinvalue(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='In questo momento 1 bitcoin vale $%d' % getBitcoinPrice() )
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
frasi_tipiche = ["Vinco sicuro!", "Caaaaaaazzz estremo!", "Sono il numero 1", "Puppatemelo sai", "Mi depilo le palle", "Oggettivamente", "Mmmm che schifo!", "Milan campione!", "Poeri poeri", "MANGIARE!", "Te lo metto nel culo!", "Indubbiamente!", "Sorto dopo cena", "Che poverta'!",
                "Se non duro due ore ti do 3000 euro", "Ue ciccia, sei bellissima", "O\' paesiello, ue ue", "Piazzami sta fia", "L\'ho giocato alla snai", "Comprate i bitcoin", "Devo comprare la McLaren", "Col cazzo, sai!", "Che fica anale", "Ti trombo nel culo!","Quest\'estate vo a Viareggio sai! M\'importa una sega",
                "Raga non insegnate al babbo a trombare", "Siete dei babbazzi!", "Trombare bere mangiare pescare guidare" ]

#frasi per dare ragione
ragione = [ "Giusto!", "Anale!", "Certo {}", "Ovviamente {}", "{} siamo i numeri uno", "Bravo {}", "Caaaaaaazzz estremo!", "{}, penso che presto saro ricco" ]
no_ragione = [ "Bravo coglione", "Ti sbagli di grosso", "Che cazzo dici", "Poveraccio", "{} guarda non commento"]
#frasi per offendere
offese = ["Non mi tritate la minchia", "Poero {}", "Col cazzo, sai!", "Puppatemelo sai", "{} puppamelo!", "Cazzo vuoi?", "{}, ora hai proprio rotto il cazzo", "{} sei un babbazzo!", "Siete dei babbazzi!", "{} guarda non commento"]
#frasi per salutare in partenza
saluti_partenza = ["Ciao, ora devo andare a trombare", "Ciao, ora devo andare a guadagnare", "Ora vado in palestra. Ciao!" ]
frasi_buongiorno = [ "Buongiorno a te {}", "{} grazie","Grazie, ora andiamo a fare soldi", "grazie {}, stai bene?", "{}, son gia in ufficio, che poverta" ]
frasi_bitcoin = ["Comprate i bitcoin, poi mi ringrazierete", "{} non vendere assolutamente i bitcoin!", "{}, penso che presto saro ricco" ]
frasi_lucia = ["Fo passare Natale e il compleanno, cosi mi fa il regalo, poi la mollo", "Ufficialmente io sono rimasto a casa, niente tag su FB", "Appena c\'ha le sue cose la lascio", "Raga ho avuto un sogno e mi sono svegliato urlando. Al prossimo mestruo la lascio" ]
frasi_roby2 = ["Che fia imperiale", "Il mese prossimo ci mettiamo insieme", "{} una fia del genere te la scordi", "Stasera se ci si vede non postate foto", "{} stasera posso venire a trombarla da te? Non ha ancora pronta la casa"]
frasi_cena_barto = ["Mangiare {}! MANGIARE!!!", "{}, imbuzzarsi!!", "Cibo!", "Ma quanto mangi {}?", "Mmmm che schifo!" ]
frasi_cena_generiche = [ "MANGIARE!", "Mangiare. MANGIAREEEE!!!!", "Imbuzzarsi!!", "Cibo!", "Ma quanto mangiate?", "MANGIARE!" ]
frasi_pesca = ["FISH!!!!", "Da vero maschio alpha" ]
frasi_macchine = ["Domenica ho il raduno", "Devo comprare la McLaren", "Ho una ferrari per le mani", "Se piazzo la ferrari faccio tanti soldi", "Devo cambiare gli ammortizzatori", "Non e\' tanto comprarla. La botta e\' sull\'assicurazione furto incendio atti vandalici e mini kasko, almeno 3500 euro annui" ]
frasi_fia = [ "Anale!", "Raga non insegnate al babbo a trombare", "Che puttana!", "Ue ciccia, sei bellissima", "Che fica anale!", "Che fica stratosferica", "{} piazzami sta fia", "La trombo nel culo", "Che delizia assoluta" ]
frasi_milan = ["Milan campione", "Ritorneremo!", "La gioco alla snai", "Si gioca contro le merde?", "Si vince sicuro" ]
frasi_moralizzatori = [ "{} mi hai rotto il cazzo. Faccio come mi pare", "{} il moralizzatore","Sono arrivati i moralizzatori", "Fatevi i cazzi vostri",
            "Si esco con due ragazze e allora? chi non le ha oggigiorno", "Da vero maschio alpha", "{} guarda ormai dal punto di vista sentimentale vivo alla giornata e faccio cio che mi va" ]
frasi_cops = [ "Poero Cops!", "Non esagerate, cops e\' molto sensibile", "Poero Cops!", "Poero Cops!" ]
frasi_stare_bene = [ "Bene", "Io sto benissimo", "Benissimo, {}", "{}, sto molto bene" ]
frasi_tie = [ "Bene sai!", "Tie!", "Godo!"]
frasi_ridere = [ "Cazzo ridi?", "{} cazzo ridi?", "Ah ah ah. Che ridere", "Sono contento vi faccia ridere", "ahahaha", "Bella questa"]
frasi_palle = ["Siete sempre piu pelosi fate schifo!", "Vi ricordo che quando ve lo puppano gli rimane i peli tra i denti a me invece leccano anche sopra il cazzo dove voi avete i peli ed è una bella sensazione che voi non conoscerete mai babbazzi"]
frasi_politica = [ "L\'Italia e\' allo sbando ed e\' tutta colpa del PD! Merdosi!", "Musulmani di merda!", "Comunisti maledetti!", "Vota Fratelli d\'Italia!" ]
frasi_segreto = ["{} non lo dire a nessuno", "Oh {}, resta tra noi. Non lo dire a nessuno"]
# traduzioni nomi
nomi_cumpa = {'Cosimo': 'Zek', 'David': 'Mazza', 'Lorenzo': 'Cops', 'Fabrizio': 'Sancio', 'Simone': 'Scarlo', 'Alessandro': 'Barto', 'L': 'Paoli', 'Francesco': 'Ciccio', 'Marco': 'Salva', 'Sandro': 'Sandrino'}

def getNomecumpa(nome):
    if nome in nomi_cumpa:
        return nomi_cumpa[nome]
    else:
        return nome
def saluta(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Ciao %s, io sto molto bene!" % getNomecumpa(update.message.from_user.first_name) )

def buongiorno(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_buongiorno).format(getNomecumpa(update.message.from_user.first_name)) )

def stobene(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_stare_bene).format(getNomecumpa(update.message.from_user.first_name)) )

def tie(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_tie).format(getNomecumpa(update.message.from_user.first_name)) )

def palle(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_palle).format(getNomecumpa(update.message.from_user.first_name)) )

def politica(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_politica).format(getNomecumpa(update.message.from_user.first_name)) )

def sparajingle(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_tipiche).format(getNomecumpa(update.message.from_user.first_name)))

def offendi(bot, update):
    offesa = random.choice(offese)
    bot.send_message(chat_id=update.message.chat_id, text=offesa.format(getNomecumpa(update.message.from_user.first_name)) )

def dare_ragione(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(ragione).format(getNomecumpa(update.message.from_user.first_name)) )

def bitcoin(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_bitcoin).format(getNomecumpa(update.message.from_user.first_name)))

def cibo(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_cena_generiche).format(getNomecumpa(update.message.from_user.first_name)))

def ridere(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_ridere).format(getNomecumpa(update.message.from_user.first_name)))

def auto(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_macchine).format(getNomecumpa(update.message.from_user.first_name)))

def calcio(bot, update):
     if re.match("^(.*)[jJ]uve(.*)$", update.message.text):
         bot.send_message(chat_id=update.message.chat_id, text="Merde!")
     else:
         bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_milan).format(getNomecumpa(update.message.from_user.first_name)))

def pesca(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_pesca).format(getNomecumpa(update.message.from_user.first_name)))

def poero(bot, update):
     if update.message.from_user.first_name == "Alessandro" or update.message.from_user.first_name == "Alex":
         poero_match = re.match(r"^.*[Pp]oero (.*)$", update.message.text, re.M|re.I)
         if poero_match:
             passbot.send_message(chat_id=update.message.chat_id, text='Davvero, {} e\' proprio un babbazzo.'.format(poero_match.group(1)))
         else:
             passbot.send_message(chat_id=update.message.chat_id, text='Hai ragione Barto')
     else:
         passbot.send_message(chat_id=update.message.chat_id, text='Mamma mia che babbazzo')

def fica(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_fia).format(getNomecumpa(update.message.from_user.first_name)))

def moralizzatori(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_moralizzatori).format(getNomecumpa(update.message.from_user.first_name)))

def lucy(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_lucia).format(getNomecumpa(update.message.from_user.first_name)))

def roby2(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_roby2).format(getNomecumpa(update.message.from_user.first_name)))

def arrivederci(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(saluti_partenza).format(getNomecumpa(update.message.from_user.first_name)) )
# quando le frasi contengono il nome del barto lui sceglie quale frase usare
# TODO: inserire una variabile per gestire i cambi di umore
def invocazione(bot, update):
    # saluta
    cumpa_match = re.match(r"^.*([Zz]ek|[Ss]ancio|[Ss]carlo|[Mm]azza|[Cc]ops).*$", update.message.text, re.M|re.I)
    if re.match("^.*[Cc]iao.*$", update.message.text):
        saluta(bot, update)
    elif re.match("^.*[Gg]razie.*$", update.message.text):
        bot.send_message(chat_id=update.message.chat_id, text="Prego {}".format(getNomecumpa(update.message.from_user.first_name)))
    elif re.match("^.*( u[Eeèé] |U[Eeèé] ).*$", update.message.text.encode('utf-8')):
        saluta(bot, update)
    elif re.match("^.*[Bb]uongiorn.*$", update.message.text.encode('utf-8')):
        buongiorno(bot, update)
    elif re.match("^(.*)[Cc]ome stai(.*)$", update.message.text):
        bot.send_message(chat_id=update.message.chat_id, text="%s, sto molto bene" % getNomecumpa(update.message.from_user.first_name) )
    elif re.match("^.*(cib|mangi| cena |ristorante|pranz|pizza|bistecca|aragosta|ostriche).*$", update.message.text):
        bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_cena_barto).format(getNomecumpa(update.message.from_user.first_name)))
    elif cumpa_match:
        offendi_match = re.match("^.*([Oo]ffendi|[Ii]nsulta|qualcosa a) .*$", cumpa_match.group())
        if offendi_match:
                nome = getNomecumpa(update.message.from_user.first_name)
                offese.append('No ' + nome + ', ' + cumpa_match.group(1) + ' e\' un amico fedele.')
                bot.send_message(chat_id=update.message.chat_id, text=random.choice(offese).format(cumpa_match.group(1), getNomecumpa(update.message.from_user.first_name)) )
        else:
                ragione_mix = [ "{0}, ha ragione {1}.", "{1}, ha ragione {0}."]
                bot.send_message(chat_id=update.message.chat_id, text=random.choice(ragione_mix).format(cumpa_match.group(1), getNomecumpa(update.message.from_user.first_name)) )
    elif re.match("^.*[Cc]oglione.*$", update.message.text) or re.match("^.*[Ss]tupido.*$", update.message.text) or re.match("^(.*)[Ff]ava(.*)$", update.message.text) or re.match("^(.*)[Ss]cemo(.*)$", update.message.text):
        offendi(bot, update)
    elif re.match("^.*[Gg]rand.*$", update.message.text) or re.match("^(.*)[Mm]mitico(.*)$", update.message.text) or re.match("^(.*)[Bb]rav(.*)$", update.message.text):
        dare_ragione(bot, update)
    elif re.match("^.*[Pp]ens.*$", update.message.text) or re.match("^.*[Dd]ico bene.*$", update.message.text) or re.match("^(.*)[Dd]ici (.*)$", update.message.text) or re.match("^(.*)[Vv]ero (.*)$", update.message.text) or re.match("^(.*)[Gg]iusto (.*)$", update.message.text):
        ragione_no_ragione = ragione + no_ragione
        bot.send_message(chat_id=update.message.chat_id, text=random.choice(ragione_no_ragione).format(getNomecumpa(update.message.from_user.first_name)) )
    elif re.match("^.*([Aa] presto|[Aa]rrivederci| a dopo).*$", update.message.text):
        arrivederci(bot, update)
    else:
        offendi(bot, update)

def segreto(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=random.choice(frasi_segreto).format(getNomecumpa(update.message.from_user.first_name)) )

updater = Updater(token='399694218:AAErsV9BZ3Oev3J334AL66jPX80MMWF1--Q')
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
# bot.send_message(emojize("Barto :moyai:", use_aliases=True))

# intercettori di testo dei messaggi
regcops = re.compile(r"^(.*)[Cc]ops(.*)$")
regmoai = re.compile(r"^(.*)"+emoji.emojize(':moyai:', use_aliases=True)+"(.*)$")
regsegreto = re.compile(r"^.*(segreto|dire.*cosa).*$")
regbitcoinvalue = re.compile(r"^.*([Qq]uanto.*val.*bitcoin).*$")
dispatcher.add_handler(RegexHandler(regcops, cops))
dispatcher.add_handler(RegexHandler(regmoai, sparajingle))
dispatcher.add_handler(RegexHandler(regsegreto, segreto))
dispatcher.add_handler(RegexHandler(regbitcoinvalue, bitcoinvalue))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Cc]olzi.*$"), colzi))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*([Cc]ome state|[Tt]utto bene).*$"), stobene))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*(macchina|lotus|ferrari|mclaren|auto).*$"), auto))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*([Mm]ilan|calcio|[Jj]uve|[Cc]hampions|[Pp]artita|[Cc]ampionato).*$"), calcio))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*(ragazza).*$"), fica))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*( fia | fica | figa | fia| figa| fica).*$"), fica))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*pesc.*$"), pesca))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Aa]nita.*$"), anita))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Aa]ttilio.*$"), attilio))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Rr]osaria.*$"), rosaria))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Rr]osalba.*$"), rosalba))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Bb]itcoin.*$"), bitcoin))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Pp]oero.*$"), poero))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*([Ll]ucy.*[Rr]oby.{0,1}2|[Rr]oby.{0,1}2.*[Ll]ucy|[Ll]ucia.*[Rr]oby.{0,1}2|[Rr]oby.{0,1}2.*[Ll]ucia).*$"), moralizzatori))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Ll]ucy.*$"), lucy))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Ll]ucia.*$"), lucy))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*([Rr]oby2|[Rr]oby 2).*$"), roby2))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*foto.*scandalo.*$"), scandalo))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*(voto|politica|Meloni|[Bb]erlusconi|Salvini).*$"), politica))
# dispatcher.add_handler(RegexHandler(re.compile(r"^(.*)[Cc]iao(.*)[Bb]arto(.*)$"), saluta))
# dispatcher.add_handler(RegexHandler(re.compile(r"^(.*)[Pp]ens(.*)[Bb]arto(.*)$"), dare_ragione))
# dispatcher.add_handler(RegexHandler(re.compile(r"^(.*)[Bb]arto(.*)$"), offendi))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*[Bb]arto.*$"), invocazione))
#altrimenti mi intercettano anche se c'è barto
dispatcher.add_handler(RegexHandler(re.compile(r"^.*(cib|mangi| cena |ristorante|pranz|pizza|bistecca|aragosta|ostriche).*$"), cibo))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*(ahah).*$"), ridere))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*(sfiga).*$"), tie))
dispatcher.add_handler(RegexHandler(re.compile(r"^.*(palle|peli|depila).*$"), palle))
# fineintercettori
# intercetta i callback
dispatcher.add_handler( CallbackQueryHandler(callbacks) )

dispatcher.add_error_handler(error)
updater.start_polling()
updater.idle()
