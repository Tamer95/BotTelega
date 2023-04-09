import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"В списке нет такой валюты {base}")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"В списке нет такой валюты {sym} ")

        if base_key == sym_key:
            raise APIException(f'Нельзя переводить одну и ту же валюту в саму себя {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не возможно обработать {amount}!')
        
        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {sym} : {new_price}"
        return message
