from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utils import main_keyboard

def quest_start(update, context):
    update.message.reply_text(
        'Как вас зовут? Напишите имя и фамилию',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'name'

def quest_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Пожалуйста, напишите имя и фамилию')
        return 'name'
    else:
        context.user_data['quest'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        update.message.reply_text(
            'Оцените бота шкале от 1 до 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 'rating'

def quest_rating(update, context):
    context.user_data['quest']['rating'] = int(update.message.text)

    update.message.reply_text(
        'Оставьте комментарий в свободной форме или пропустите этот шаг, введя /skip'
    )
    return 'comment'

def quest_comment(update, context):
    context.user_data['quest']['comment'] = update.message.text
    user_text = quest_format(context.user_data['quest'])

    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def quest_skip(update, context):
    user_text = quest_format(context.user_data['quest'])

    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def quest_format(user_quest):
    user_text = f"""<b>Имя Фамилия:</b> {user_quest['name']}
<b>Оценка:</b> {user_quest['rating']}"""
    if 'comment' in user_quest:
        user_text += f"\n<b>Комментарий:</b> {user_quest['comment']}"
 
    return user_text

def quest_wtf(update, context):
    update.message.reply_text("Не понимаю :(")