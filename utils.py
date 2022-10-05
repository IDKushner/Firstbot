from glob import glob
from telegram import ReplyKeyboardMarkup
from random import choice
from emoji import emojize
import Settings

def main_keyboard():
    return ReplyKeyboardMarkup([['Котик!']])

def get_smile(user_data): # функция присваивает пользователю случайный смайлик из списка и потом возвращает только его (до перезапуска бота)
    if 'emoji' not in user_data: # user_data это встроенный словарь с информацией о юзере, который обновляется при перезапуске бота
        smile = choice(Settings.USER_EMOJI)
        return emojize(smile, language='alias') # language='alias' позволяет называть смайлики по текстовому псевдониму с двоеточием
    return user_data['emoji']    
