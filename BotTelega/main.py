import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

exchanges = {'доллар':'USD', 'евро': 'EUR', 'рубль': 'RUB'}

TOKEN = "6088991461:AAGK5QWaGWSIvn0pJsByxw_VLDfLh-DicCs"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])

def start(message: telebot.types.Message):
    text = (
        "Привет! Я могу помочь тебе конвертировать валюты. \n"
        "Чтобы начать работу, введи команду в следующем формате:\n"
        "<имя валюты цену которой хотите узнать> "
        "<имя валюты в которой надо узнать цену первой валюты> "
        "<количество первой валюты>. \n"
        "Чтобы увидеть список всех доступных валют, введи команду /values. \n"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) > 3:
            raise APIException('Ввели слишком много запросов')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Что-то пошло не так, пжл перезагрузите бота:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
