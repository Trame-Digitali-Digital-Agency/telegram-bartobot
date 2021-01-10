import json
import requests

def generaMeme():
    URL = "https://meme-api.herokuapp.com/gimme"
    try:
        r = requests.get(URL)
        imgUrl = json.loads(r.text)["preview"][-1]
        return imgUrl
    except requests.ConnectionError:
        return "Reddit API non va"

print(generaMeme())