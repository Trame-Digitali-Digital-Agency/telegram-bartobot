import json
import requests
from googletrans import Translator

def quoteTrump():
	URL = "https://www.tronalddump.io/random/quote"
	try:
		r = requests.get(URL)
		quote = json.loads(r.text)["value"]
	except requests.ConnectionError:
		return "Tronalddump non va"
	translator = Translator()
	print(quote)
	translated = translator.translate(quote, src='en', dest='it')
	return translated.text

print(quoteTrump())