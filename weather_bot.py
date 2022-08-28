import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
import requests

api_key = '352474be0834577f75c26403cdcebebf'
bot = Bot(token = "5326539302:AAEQ1_NWFsAZO-TLdH_Ovr2F_FSrTa7Czg8")

dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=("start"))
async def send_hello(message: types.Message):
    await message.answer("Привет, другалечек!\nЕсли хочешь узнать сводку погоды, тогда вводи название города: ")


@dp.message_handler()
async def get_weathers(message: types.Message):
    lang_ru = {
        "Clear": "Ясно",
        "Clouds": "Облачно",
        "Rain": "Дождь",
        "Drizzle": "Морось",
        "Thunderstorm": "Гроза",
        "Snow": "Снег",
        "Mist": "Туман"
    }
    try:
        req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={api_key}&units=metric')
        data = req.json()
        city_name = data['name']
        cur_weather = data['main']['temp']
        wind = data['wind']['speed']
        weather_description = data['weather'][0]['main']
        if weather_description in lang_ru:
            wd = lang_ru[weather_description]
        else:
            wd = 'Посмотри в окно, погода не опознана :('
        humidity = data['main']['humidity']
        temp_max = data['main']['temp_min']
        temp_min = data['main']['temp_max']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        await message. answer(f'Погода в городе: {message.text}\n'
            f'Температура воздуха: {cur_weather}' + ' °C\n' 
            f'Сейчас: {wd}\n'
            f'Влажность: {humidity}' + '%''\n'
            f'Скорость ветра: {wind}' + " м/с\n"
            f'Максимальная температура: {temp_min}' + ' °C\n'                  
            f'Минимальная температура: {temp_max}' + ' °C\n'
            f'Восход солнца: {sunrise}\n'
            f'Закат солнца: {sunset}\n'
              )
    except:
        await message.answer('Что-то не так...\nПроверьте название города!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
