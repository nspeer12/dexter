import requests
import inflect


def bitcoin_price(query:str, context):
    

    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()

    price = data["bpi"]["USD"]["rate"]
    price = price.split(".")[0]

    infl = inflect.engine()

    ans = "The current price of bitcoin is "
    ans += infl.number_to_words(price)
    ans += ' dollars'

    return ans