from utils import *
from glob import glob
import os

def greet_user(update, context):
    print('Вызван \start')
    if 'emoji' in context.user_data:
        del context.user_data['emoji'] 
    update.message.reply_text(
        'Привет, пользователь! Ты вызвал команду /start',
        reply_markup=main_keyboard()
        )

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f'{text} {context.user_data["emoji"]}', 
        reply_markup=main_keyboard()
        )

def send_cat(update, context):
    img = (choice(glob('images/cat*.jp*g'))) # "*" ознаачает, что на её месте в этой функции может стоять что угодно
    chat_id = update.effective_chat.id # получаем id текущего чата с пользователем, чтобы отправить туда картинку
    context.bot.send_photo(chat_id=chat_id, photo=open(img, 'rb'))

def count_words(update, context):
    text = update.message.text
    print(text)
    if len(context.args) == 0:
        update.message.reply_text(
            'Вы забыли текст :)',
            reply_markup=main_keyboard()
            )
    else:
        update.message.reply_text(
            f'количество слов: {len(context.args)}',
            reply_markup=main_keyboard()
            )

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
        ans_word = choice(cities)
        update.message.reply_text(f'{ans_word}. Тебе на {ans_word[-1].upper()}')
        del unused_cities[ans_word[0]][ans_word]

def calc(update, context):
    try:
        value = context.args
        # в переменную context.args в виде списка записывается всё, что идёт после пробела после команды с удаленными лишним пробелами:
        # т.е. если ввести "/calc 143 +  35", то там будет ['143', '+', '35']
            
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

def check_user_photo(update, context):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text("Файл сохранен")
    if has_object_on_image(filename, 'dog'):
        # посколько мы добавили этой ф-ции 2й параметр, нужно теперь добавлять, что на картинке надо найти/заставить пользователя это задавать
        # проверить завтра можно ли создать а потом удалить MessageHandler(Filters.text), чтобы передать название объекта в эту функцию
        update.message.reply_text("Обнаружен объект, добавляю в библиотеку.")
        new_filename = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Тревога, объект не обнаружен!")