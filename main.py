import telebot 
from config import token
from random import randint
from logic import Pokemon, Wizard, Fighter  # Убедитесь, что вы импортируете необходимые классы

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def start(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона.")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        enemy_username = message.reply_to_message.from_user.username
        user_username = message.from_user.username
        
        if enemy_username in Pokemon.pokemons.keys() and user_username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[enemy_username]
            pok = Pokemon.pokemons[user_username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами.")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщение того, кого хочешь атаковать.")

@bot.message_handler(commands=['info'])
def info(message):
    # Проверяем, есть ли у пользователя покемон
    if message.from_user.username in Pokemon.pokemons.keys():
        # Получаем покемона пользователя
        pok = Pokemon.pokemons[message.from_user.username]
        # Отправляем информацию о покемоне
        bot.send_message(message.chat.id, pok.info())
    else:
        bot.send_message(message.chat.id, "У тебя нет покемона. Создай его с помощью команды /go.")

@bot.message_handler(commands=['feed'])
def feed_pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        pok.feed()  # Метод кормления покемона
        bot.send_message(message.chat.id, f"{pok.name} был покормлен! Уровень счастья: {pok.happiness}")
    else:
        bot.send_message(message.chat.id, "У тебя нет покемона. Создай его с помощью команды /go.")

# Запуск бота
bot.infinity_polling(none_stop=True)
