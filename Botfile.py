import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import Settings
from random import randint

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван \start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def count_words(update, context):
    text = update.message.text
    print(text)
    if len(text.split()[1:]) == 0:
        update.message.reply_text('Вы забыли текст :)')
    else:
        update.message.reply_text(f'количество слов: {len(text.split()[1:])}')

def cities_game(update, context):
    cities_list = {
        'А': ['Алматы', 'Астана', 'Альтаир'], 
        'Б': ['Брест', 'Белгород', 'Белокаменск'], 
        'В': ['Воронеж', 'Волоколамск', 'Выхино']
        }
    word = update.message.text
    print(word)
    start_letter = word[0].upper()
    letter = word[-1].upper()

    if letter not in list(cities_list.keys()):
        update.message.reply_text('Извини, я больше не знаю слов на эту букву :(')
    else:
        if start_letter in cities_list:
             if word in cities_list[start_letter]:
                del cities_list[start_letter][word]
                
    list_of_cities = cities_list[letter]
    ans_word = list_of_cities[randint(0, len(list_of_cities) - 1)]
    update.message.reply_text(f'{ans_word}. Тебе на {ans_word[-1].upper()}')
    del cities_list[ans_word[0]][ans_word]

def main():
    bot = Updater(Settings.API_KEY)

    dp = bot.dispatcher # ввожу переменную просто чтобы не писать каждый раз "bot.dispatcher"
    dp.add_handler(CommandHandler('start', greet_user)) # добавляю диспетчеру бота обработчик CommandHandler, которому задаю реакцию на команду start
    dp.add_handler(CommandHandler('wordcount', count_words))
    dp.add_handler(CommandHandler('cities', cities_game))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # попробовать добавить MessageHandler в cities_game + стоп-слово для игры, например "Стоп"

    logging.info('Bot started')

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()