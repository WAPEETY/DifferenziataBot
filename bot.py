import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from time import sleep
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


    # Se l'utente ha configurato tutto
    if user.status == "normal":
        if text == "/start":
            bot.sendMessage(chatId, "Bentornato, <b>{0}</b>!\n"
                                    "Cosa posso fare per te?".format(name), parse_mode="HTML")

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
        bot.editMessageText((chatId, message_id), "Ottimo. Qual'è il tuo tipo di raccolta?")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Utenze domestiche", callback_data="typeDOM#{0}".format(message_id))
        ],
        [
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

# Mantieni il bot in esecuzione
while True:
    sleep(60)
