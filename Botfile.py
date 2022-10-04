import logging
from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import Settings
from random import randint, choice
from glob import glob

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван \start')
    if 'emoji' in context.user_data:
        del context.user_data['emoji'] 
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f'{text} {context.user_data["emoji"]}')

def get_smile(user_data): # функция присваивает пользователю случайный смайлик из списка и потом возвращает только его (до перезапуска бота)
    print(user_data)
    if 'emoji' not in user_data: # user_data это встроенный словарь с информацией о юзере, который обновляется при перезапуске бота
        smile = choice(Settings.USER_EMOJI)
        return emojize(smile, language='alias') # language='alias' позволяет называть смайлики по текстовому псевдониму с двоеточием
    return user_data['emoji']

def count_words(update, context):
    text = update.message.text
    print(text)
    if len(context.args) == 0:
        update.message.reply_text('Вы забыли текст :)')
    else:
        update.message.reply_text(f'количество слов: {len(context.args)}')

def cities_game(update, context): # Непонятно почему не работает :(
    cities_list = {
        'А': ['Алматы', 'Астана', 'Альтаир'], 
        'Б': ['Брест', 'Белгород', 'Белокаменск'], 
        'В': ['Воронеж', 'Волоколамск', 'Выхино']
        }
    unused_cities = cities_list.copy()
    used_cities = []
    word = context.args[0]
    print(word)
    
    start_letter = word[0].upper()
    letter = word[-1].upper()

    if word in used_cities:
        update.message.reply_text('Этот город уже был. Введи новый')
    else:
        if word in unused_cities[start_letter]:
            used_cities.append(unused_cities[start_letter][word])
            print(used_cities) #!!
            del unused_cities[start_letter][word]
            print(unused_cities) #!!

    if len(unused_cities[letter]) == 0:
        update.message.reply_text('Извини, я больше не знаю слов на эту букву :(') 
    else:           
        cities = unused_cities[letter]
        ans_word = cities[randint(0, len(cities) - 1)]
        update.message.reply_text(f'{ans_word}. Тебе на {ans_word[-1].upper()}')
        del unused_cities[ans_word[0]][ans_word]

def calc(update, context):
    try:
        value = context.args
        # в переменную context.args в виде списка записывается всё, что идёт после пробела после команды с удаленными лишним пробелами:
        # т.е. если ввести "/calc 143 +  35", то там будет ['143', '+', '35']
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

def send_cat(update, context):
    img = (choice(glob('images/cat*.jp*g'))) # "*" ознаачает, что на её месте в этой функции может стоять что угодно
    chat_id = update.effective_chat.id # получаем id текущего чата с пользователем, чтобы отправить туда картинку
    context.bot.send_photo(chat_id=chat_id, photo=open(img, 'rb'))

def main():
    bot = Updater(Settings.API_KEY)

    dp = bot.dispatcher # ввожу переменную просто чтобы не писать каждый раз "bot.dispatcher"
    dp.add_handler(CommandHandler('start', greet_user)) # добавляю диспетчеру бота обработчик CommandHandler, которому задаю реакцию на команду start
    dp.add_handler(CommandHandler('wordcount', count_words))
    dp.add_handler(CommandHandler('cities', cities_game))
    dp.add_handler(CommandHandler('calc', calc))
    dp.add_handler(CommandHandler('cat', send_cat))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # попробовать добавить MessageHandler в cities_game + стоп-слово для игры, например "Стоп"

    logging.info('Bot started')

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()