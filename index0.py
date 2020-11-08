import requests

# raccolgo nella variabile `testo` ciò che gli utenti scriveranno in chat al bot
testo=Hook['params']['message']['text']

# raccolgo la chat ID
chatID=Hook['params']['message']['chat']['id']

# imposto l'URL per inviare i messaggi indietro al bot
URL='https://api.telegram.org/bot' + Hook['env']['parrot_bot_key'] + '/sendMessage'

# invio indietro alla chat ID il messaggio ricevuto
richiesta=requests.get(URL,verify=False,data={'chat_id':chatID,'text':testo})
