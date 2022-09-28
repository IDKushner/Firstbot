import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import Settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван \start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    bot = Updater(Settings.API_KEY)

    dp = bot.dispatcher # ввожу переменную просто чтобы не писать каждый раз "bot.dispatcher"
    dp.add_handler(CommandHandler('start', greet_user)) # добавляю диспетчеру бота обработчик CommandHandler, которому задаю реакцию на команду start
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot started')

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()