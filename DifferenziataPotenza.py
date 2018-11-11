import telepot
from time import sleep
from config import TOKEN

bot = telepot.Bot(TOKEN)
area_raccolta = 0
tipo_raccolta = 0

def riceve_messaggio(msg):
    global area_raccolta
    msgType, chatType, chatId = telepot.glance(msg)
    text = str(msg['text'])

    print("Tipo messaggio: {0}\n"
          "Tipo chat: {1}\n"
          "ChatID: {2}".format(msgType, chatType, chatId))

    if text.lower() == "area urbana":
        area_raccolta = 0
        bot.sendMessage(chatId, "Hai selezionato: Area urbana")
        print("Tipo raccolta: {0}".format(area_raccolta))

    elif text.lower() == "area industriale":
        area_raccolta = 1
        bot.sendMessage(chatId, "Hai selezionato: Area industriale")
        print("Tipo raccolta: {0}".format(area_raccolta))

    elif text.lower() == "area extraurbana" or text.lower() == "area extra urbana":
        area_raccolta = 2
        bot.sendMessage(chatId, "Hai selezionato: Area extraurbana")
        print("Tipo raccolta: {0}".format(area_raccolta))
    if text.lower() == "utenze domestiche":
        tipo_raccolta = 0
        bot.sendMessage(chatId, "Hai selezionato: Utenze domestiche")
        print("Tipo utenza: {0}".format(tipo_raccolta))
    elif text.lower() == "utenze non domestiche":
        tipo_raccolta = 1
        bot.sendMessage(chatId, "Hai selezionato: Utenze non domestiche")
        print("Tipo utenza: {0}".format(tipo_raccolta))
    

bot.message_loop({'chat': riceve_messaggio})

while True:
    sleep(60)
