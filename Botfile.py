import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import Settings

from handlers import * 
from quest import *

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    bot = Updater(Settings.API_KEY)

    dp = bot.dispatcher # ввожу переменную просто чтобы не писать каждый раз "bot.dispatcher"

    quest = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), quest_start)
        ], 
        states={
            'name': [MessageHandler(Filters.text, quest_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), quest_rating)],
            'comment': [
                CommandHandler('skip', quest_skip),
                MessageHandler(Filters.text, quest_comment)
            ]
        }, 
        fallbacks=[
            MessageHandler(
                Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, quest_wtf
            )
        ]
    )

    dp.add_handler(quest)
    dp.add_handler(CommandHandler('start', greet_user)) # добавляю диспетчеру бота обработчик CommandHandler, которому задаю реакцию на команду start
    dp.add_handler(CommandHandler('wordcount', count_words))
    dp.add_handler(CommandHandler('cities', cities_game))
    dp.add_handler(CommandHandler('calc', calc))
    dp.add_handler(CommandHandler('cat', send_cat))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.regex('^(Котик!)$'), send_cat))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # попробовать добавить MessageHandler в cities_game + стоп-слово для игры, например "Стоп"
    # dp.remove_handler(?)
    logging.info('Bot started')

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()