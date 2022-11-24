import logging

from aiogram import Bot, Dispatcher, executor, types
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token="5699589042:AAHwmhaK-zuT8w_QxINVHgFCJHt3ii12u0A")     #Бот токен
dp = Dispatcher(bot)
db = Database("database.db") #База данных

users = db.get_users()
CHANNEL_ID = [db.get_users()]

#Комнда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private' or 'channel' or 'group':      #Как только бот видит старт он записывает нновго пользователя в БД
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "Welcome to hell beatch))")

        if message.from_user.id == 500812989 or 230216005:    #Админы

            if not db.user_exists(message.chat.id):
                   db.add_user(message.chat.id)
                   await bot.send_message(message.chat.id, "Welcome to hell beatch))")

        else:
            await bot.send_message(message.from_user.id, "Бот запущен")

        #await bot.send_message(message.from_user.id, "Welcome to hell beatch))")


#@dp.message_handler(commands=['start@FrAnstbot'])
#async def chat(message: types.Message):
    #if message.chat.type == 'private':
        #if not db.user_exists(message.chat.id):
            #db.add_user(message.chat.id)

        #await bot.send_message(message.from_user.id, "GG")


#/help
@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Разослать всем сообщения /sendall \n Разослать фото - просто закинуть фото в чат")

#Отправка фото
@dp.message_handler(content_types=['photo'])
async def send_photo(message: types.Message):
    if message.chat.type == 'private' or 'channel' or 'group':
        if message.from_user.id == 500812989 or 230216005:

           photo_id = message.photo[-1].file_id  #Массив для фотки
           users = db.get_users()
           for row in users:
               try:
                   await bot.send_photo(row[0], photo_id)    #Если человек в БД разсыдает фотки
                   if int(row[1]) != 1:
                       db.set_active(row[0], 1)

                   await bot.send_photo(message.from_user.id, photo_id)
                   await bot.send_photo(CHANNEL_ID, photo_id)

               except:
                   db.set_active(row[0], 0)

           #await bot.send_photo(message.from_user.id, photo_id)
           #await bot.send_photo(CHANNEL_ID , photo_id)

    #await bot.send_message(message.from_user.id, "В разработке")

#Рассылка все сообщений
@dp.message_handler(commands=["sendall"])
async def sendall(message: types.Message):
    if message.chat.type == 'private' or 'channel' or 'group':
        if message.from_user.id == 500812989 or 230216005:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)  #Если получилось доставить смс, то в бд алгоритм отмечает пользователя как активного
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)

                except:
                    db.set_active(row[0], 0)  #Иначе как неактивного

            await bot.send_message(message.from_user.id, "Успешно")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
