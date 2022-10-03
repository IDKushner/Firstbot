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

def calc(update, context):
    s = update.message.text
    try: 
        value = list(str(s).replace(' ', '')[5:]) 
        # убираем из строки /команду и пробелы, выделяем каждый символ
        # но таким методом многоцифорные числа будут набором отдельных чисел (143 -> '1', '4', '3'), их надо соединить обратно
            
        temp = [] 
        s = ''
        for symbol in value:
            if symbol not in '+-/*':
                s += symbol
            else:
                temp.append(s)
                s = ''
                temp.append(symbol)
        temp.append(s)
            
        value = list(map(lambda x: float(x) if x.replace('.', '').isdigit() == True else x, temp))

        while '*' in value or '/' in value:
            if '*' in value:
                mult_ind = value.index('*')
            else:
                mult_ind = 0
            if '/' in value:
                div_ind = value.index('/')
            else:
                div_ind = 0
            if mult_ind > div_ind:
                value[mult_ind - 1 : mult_ind + 2] = [value[mult_ind - 1] * value[mult_ind + 1]]
                # заменяем срез [один символ до знака операции : один символ после знака операции] на результат операции
                # например заменяем [5, '*', 3] на [15]
            else: 
                value[div_ind - 1 : div_ind + 2] = [value[div_ind - 1] / value[div_ind + 1]]
                    
        while '+' in value or '-' in value:
            if '+' in value:
                sum_ind = value.index('+')
            else:
                sum_ind = 0
            if '-' in value:
                ded_ind = value.index('-')
            else:
                ded_ind = 0
            if sum_ind > ded_ind:
                value[sum_ind - 1 : sum_ind + 2] = [value[sum_ind - 1] + value[sum_ind + 1]]
            else:
                value[ded_ind - 1 : ded_ind + 2] = [value[ded_ind - 1] - value[ded_ind + 1]]

        return update.message.reply_text(round(float(value[0]), 2))
        
    except ZeroDivisionError:
        return update.message.reply_text('На ноль делить нельзя!')
    except:
        return update.message.reply_text('Кажется, где-то ошибка :(')    

def main():
    bot = Updater(Settings.API_KEY)

    dp = bot.dispatcher # ввожу переменную просто чтобы не писать каждый раз "bot.dispatcher"
    dp.add_handler(CommandHandler('start', greet_user)) # добавляю диспетчеру бота обработчик CommandHandler, которому задаю реакцию на команду start
    dp.add_handler(CommandHandler('wordcount', count_words))
    dp.add_handler(CommandHandler('cities', cities_game))
    dp.add_handler(CommandHandler('calc', calc))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # попробовать добавить MessageHandler в cities_game + стоп-слово для игры, например "Стоп"

    logging.info('Bot started')

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()