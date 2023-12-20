import os
import webbrowser
import sys
import subprocess
import requests
import voices


def youtubebrowser():
    webbrowser.open('https://www.youtube.com', new=2)


def musicbrowser():
    webbrowser.open('https://vk.com/audios617969371')


def music():
    subprocess.Popen('C:/Users/Tercia/AppData/Roaming/Spotify/Spotify.exe')


def game():
    try:
        subprocess.Popen('D:/gayshit/shapezaa2PF/shapezio.exe')
    except:
        voices.speaker_silero('Установи свой путь расположения к игре.')


def offpc():
    # Эта команда отключает ПК под управлением Windows
    voices.speaker_silero('ДАсвидОс!')

    os.system('shutdown /s')
    # voice.speaker('Компьютер был бы выключен, но команда в коде отключена')


def offBot():
    sys.exit(1)


def weather():
    '''Для работы этого кода нужно зарегистрироваться на сайте
    https://openweathermap.org или переделать на ваше усмотрение под что-то другое'''
    try:
        params = {'q': 'Orenburg', 'units': 'metric',
                  'lang': 'ru', 'appid': os.getenv("WEATHER_API_KEY")}
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        voices.speaker_gtts(
            f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

    except:
        voices.speaker_silero(
            'Произошла ошибка при попытке запроса к ресурсу, проверь код')


def passive():
    pass
