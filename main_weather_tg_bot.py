import requests
from datetime import datetime
from config import tg_bot_token, open_weather_token
import telebot


bot = telebot.TeleBot(token=tg_bot_token)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет!, Напиши мне название города и я пришлю сводку погоды!')


@bot.message_handler()
def get_weather(message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода!'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(
            data['sys']['sunrise'])

        bot.send_message(message.chat.id, f'***{datetime.now().strftime(r'%Y-%m-%d %H:%M')}***\n'
              f'Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n'
              f'Влажность: {humidity}%\nДавление: {pressure}мм.рт.ст\n'
              f'Скорость ветра: {wind}м/c\nВосход солнца: {sunrise_timestamp}\n'
              f'Закат солнца: {sunset_timestamp}\nПродолжительность часового дня: {length_of_the_day}\n'
              f'***Хорошего дня!***'
              )

    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, '\U00002620 Проверьте название города \U00002620')


if __name__ == '__main__':
    bot.polling()