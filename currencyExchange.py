from requests import get
from pprint import PrettyPrinter

BASE_URL = ""
API_KEY = ""

printer = PrettyPrinter()

def get_currencies():
    endpoint = f""
    url = BASE_URL + endpoint
    response = get(url, timeout=60).json()["results"]
    data = list(response.items())
    data.sort()
    return data
def print_currecies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f""
    url = BASE_URL + endpoint
    data = get(url, timeout=60).json()
    if len(data) == 0:
        print('Invalid currencies')
        return
    return list(data.values())[0]
    
    

#data = get_currencies()
#print_currecies(data)


