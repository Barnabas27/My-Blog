import requests,json

def get_random_quotes():
    r = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    if r.status_code == 200:
        quote = r.json()
        return quote