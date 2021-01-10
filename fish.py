import logging
import random
import re
import emoji
import json
import requests
from pprint import pprint
from urllib.request import urlopen
import datetime, time

# from lib import asciigen
# asciigen.from_filename('./python-logo.png', width=40, contrast=1.8)
from googletrans import Translator

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

fish = infoPesce()
print("Conoscete il %s ?" % fish["Species Name"].text)
print(fish["url"])

print(fish["Physical Description"].text)
print(fish["Biology"].text)
print("\n\n")
print(fish["Habitat"].text)
print(fish["Habitat Impacts"].text)
print(fish["Fishing Rate"].text)
print("\n\n Se vi interessa mangiarlo sappiate che:")
print(fish["Taste"].text)
