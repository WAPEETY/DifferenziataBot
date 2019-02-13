#!/usr/bin/env python3

import telepot
import sqlite3
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.exception import TelegramError, BotWasBlockedError
from time import sleep
from time import localtime
from pony.orm import db_session, select, exists
from modules.database import User, db

# Controlla per il file token.txt
try:
    f = open('token.txt', 'r')
    token = f.readline().strip()
    f.close()
except FileNotFoundError:
    token = input("File 'token.txt' not found. Please insert the Bot API Token: ")
    f = open('token.txt', 'w')
    f.write(token)
    f.close()

bot = telepot.Bot(token)


# Rispondi ad un messaggio
@db_session
def reply(msg):
    msgType, chatType, chatId = telepot.glance(msg)
    name = msg['from']['first_name']
    try:
        text = msg['text']
    except ValueError:
        text = ""

    # Se l'utente non è nel database, inseriscilo
    if not User.exists(lambda u: u.chatId == chatId):
        User(chatId=chatId, status="new")

    user = User.get(chatId=chatId)

    #donazioni
    if text == "/dona":
        bot.sendMessage(chatId, "Ecco qui il mio link PayPal, Grazie mille! \n"
                                "https://www.paypal.me/wapeetyofficial")

    #aiuto

    if text == "/aiuto":
        bot.sendMessage(chatId, "Ecco qui i vari comandi disponibili \n"
                                "/configura - Se non hai ancora configurato il bot \n"
                                "/cancella - Se hai sbagliato a configurare il bot o vuoi cancellare la tua configurazione \n"
                                "/dona - Se dovessi sentirti tanto buono da donare qualcosina (offerta libera) \n"
                                "/aiuto - Per mostrare questo messaggio")

    # Se l'utente ha configurato tutto
    if user.status == "normal":
        if text == "/start":
            bot.sendMessage(chatId, "Bentornato, <b>{0}</b>!\n"
                                    "Da quanto tempo!".format(name), parse_mode="HTML")

        elif text == "/configura":
            bot.sendMessage(chatId, "Non c'è bisogno di configurarmi, hai già fatto tutto!")
        elif text == "/cancella":
            sent = bot.sendMessage(chatId, "Vuoi cancellare i tuoi dati per sempre? (questa azione é irreversibile)")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Si", callback_data="del_yes#{0}".format(sent['message_id'])),
                InlineKeyboardButton(text="No", callback_data="del_no#{0}".format(sent['message_id']))
            ]])
            bot.editMessageReplyMarkup((chatId, sent['message_id']), keyboard)


    # Se l'utente deve ancora inserire i dati
    elif user.status == "new":
        if text == "/start":
            bot.sendMessage(chatId, "Benvenuto, <b>{0}</b>!\n"
                                    "Per iniziare, premi /configura.".format(name), parse_mode="HTML")

        elif text == "/configura":
            user.status = "getting_area"
            sent = bot.sendMessage(chatId, "OK! Per iniziare, scegli la tua area di raccolta.", reply_markup=None)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Area urbana", callback_data="areaURB#{0}".format(sent['message_id'])),
                InlineKeyboardButton(text="Area industriale", callback_data="areaIND#{0}".format(sent['message_id']))
            ],
            [
                InlineKeyboardButton(text="Area extraurbana", callback_data="areaEXT#{0}".format(sent['message_id']))
            ]])
            bot.editMessageReplyMarkup((chatId, sent['message_id']), keyboard)


@db_session
def button_press(msg):
    query_id, chatId, query_data = telepot.glance(msg, flavor="callback_query")
    user = User.get(chatId=chatId)
    query_split = query_data.split("#")
    message_id = int(query_split[1])
    button = query_split[0]

    if user.status == "getting_area":
        if button == "areaURB":
            user.area_raccolta = "URB"

        elif button == "areaIND":
            user.area_raccolta = "IND"

        elif button == "areaEXT":
            user.area_raccolta = "EXT"

        user.status = "getting_type"
        if user.area_raccolta != "EXT":
            bot.editMessageText((chatId, message_id), "Ottimo. Qual'è il tuo tipo di raccolta?")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Utenze domestiche", callback_data="typeDOM#{0}".format(message_id))
            ],
            [
                InlineKeyboardButton(text="Utenze NON domestiche", callback_data="typeNOTDOM#{0}".format(message_id))
            ]])
            bot.editMessageReplyMarkup((chatId, message_id), keyboard)
        else:
            bot.editMessageText((chatId, message_id), "Ottimo. Qual'è il tuo tipo di raccolta?")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Utenze NON domestiche", callback_data="typeNOTDOM#{0}".format(message_id))
            ]])
            bot.editMessageReplyMarkup((chatId, message_id), keyboard)

    elif user.status == "getting_type":
        if button == "typeDOM":
            user.tipo_raccolta = "DOM"

        elif button == "typeNOTDOM":
            user.tipo_raccolta = "NOTDOM"

        user.status = "normal"

        bot.editMessageReplyMarkup((chatId, message_id), None)
        bot.editMessageText((chatId, message_id), "Fatto!")

    elif user.status == "normal":
        if button == "del_yes":
            user.area_raccolta = ""
            user.tipo_raccolta = ""
            user.status = "new"
            bot.editMessageReplyMarkup((chatId, message_id), None)
            bot.editMessageText((chatId, message_id), "Fatto, per configurare il tutto usa il comando /configura")
        elif button == "del_no":
            bot.editMessageReplyMarkup((chatId, message_id), None)
            bot.editMessageText((chatId, message_id), "OK, sono contento che userai ancora il bot!")

bot.message_loop({'chat': reply, 'callback_query': button_press})


@db_session
def trash_notify():
    '''This function sends the shitty notification to each
    "normal" fucking user in the database at 8:00 PM.

    I need the fucking types too, but I don't know it, so I'll create
    an empty dictionary and make the owner complete it.
    '''
    
    tm = localtime()            # imposta la variabile tm all'orario locale
    type_trash = {
        'URB': { #io
            'typeDOM': {
                0: 'Indifferenziata',                               # Monday
                1: 'Plastica e metalli',                            # Tuesday
                2: 'Organico, Vetro',                               # Wednesday
                3: 'Carta e cartone',                               # Thursday
                4: 'Organico',                                      # Friday
                5: 'Nulla',                                         # Sathurday
                6: 'Organico',                                      # Sunday
            },

            'typeNOTDOM': { #guarino
                0: 'Indifferenziata e vetro',                       # Monday
                1: 'Plastica e metalli, Carta e cartone',           # Tuesday
                2: 'Organico, Vetro',                               # Wednesday
                3: 'Carta e cartone',                               # Thursday
                4: 'Organico, Plastica e metalli',                  # Friday
                5: 'Nulla',                                         # Sathurday
                6: 'Organico, Plastica e metalli, Carta e cartone', # Sunday
            }
        },

        'IND': {
            'typeDOM': { #mi fra
                0: 'Organico, Plastica e Metalli, Cartone',          # Monday
                1: 'Indifferenziata, Vetro',                         # Tuesday
                2: 'Plastica e metalli, Cartone',                    # Wednesday
                3: 'Organico, Vetro',                                # Thursday
                4: 'Carta e cartone',                                # Friday
                5: 'Organico, Plastica e metalli',                   # Sathurday
                6: 'Nulla',                                          # Sunday
            },

            'typeNOTDOM': { #magro
                0: 'Organico, Plastica e Metalli, Cartone',          # Monday
                1: 'Indifferenziata, Vetro',                         # Tuesday
                2: 'Plastica e metalli, Cartone',                    # Wednesday
                3: 'Organico, Vetro',                                # Thursday
                4: 'Carta e cartone',                                # Friday
                5: 'Organico, Plastica e metalli',                   # Sathurday
                6: 'Nulla',                                          # Sunday
            }
        },

        'EXT': {
            'typeDOM': { #di melfi
                0: 'Dato non disponibile',                           # Monday
                1: 'Dato non disponibile',                           # Tuesday
                2: 'Dato non disponibile',                           # Wednesday
                3: 'Dato non disponibile',                           # Thursday
                4: 'Dato non disponibile',                           # Friday
                5: 'Dato non disponibile',                           # Sathurday
                6: 'Dato non disponibile',                           # Sunday
            },

            'typeNOTDOM': { #sileo
                0: 'Indifferenziata, Vetro',                         # Monday
                1: 'Plastica e metalli, Carta e cartone',            # Tuesday
                2: 'Organico, Vetro',                                # Wednesday
                3: 'Carta e cartone',                                # Thursday
                4: 'Organico, Plastica e metalli',                   # Friday
                5: 'Nulla',                                          # Sathurday
                6: 'Carta e cartone',                                # Sunday
            }
        }
    }
    
    if tm.tm_hour == 20 and tm.tm_min == 00: # verifica se sono le 20:00
        # definisce il giorno
        shitty_day = tm.tm_wday
        # connessione al DB
        db_connection = sqlite3.connect('differenziatabot.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT * FROM User WHERE status = "normal"')
        db_rows = db_cursor.fetchall()
    
        # invia la notifica ad ogni utente "normale" nel database 
        try:
            for row in db_rows:
                bot.sendMessage(row[1], 'Oggi devi buttare {}'.format(type_trash[row[3]]['type' + row[4]][shitty_day]))
        except Exception as error_msg:
            db_cursor.execute('DELETE FROM User WHERE chatId = {}'.format(row[0]))
            with open('logfile.txt', 'a') as log_file:
                log_file.write('Niroge is stupid -> {}\n'.format(error_msg))
    return
    
# Mantieni il bot in esecuzione
while True:
    sleep(60)                   # Controlla ogni minuto che ore sono
    trash_notify()
