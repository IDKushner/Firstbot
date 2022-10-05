import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import Settings

from handlers import * 

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    bot = Updater(Settings.API_KEY)

    dp = bot.dispatcher # ввожу переменную просто чтобы не писать каждый раз "bot.dispatcher"
    dp.add_handler(CommandHandler('start', greet_user)) # добавляю диспетчеру бота обработчик CommandHandler, которому задаю реакцию на команду start
    dp.add_handler(CommandHandler('wordcount', count_words))
    dp.add_handler(CommandHandler('cities', cities_game))
    dp.add_handler(CommandHandler('calc', calc))
    dp.add_handler(CommandHandler('cat', send_cat))
    dp.add_handler(MessageHandler(Filters.regex('^(Котик!)$'), send_cat))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # попробовать добавить MessageHandler в cities_game + стоп-слово для игры, например "Стоп"

    logging.info('Bot started')

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()