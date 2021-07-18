import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackQueryHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s '
                           '- %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Здороваемся"""
    update.message.reply_text('Привет! Я бот, который очень любит котиков '
                              'и подарит тебе хорошее настроение '
                              ':3\nНапиши мне /cat и я отправлю тебе котика!')


def help_me(update):
    """Прописываем помощь с командами"""
    update.message.reply_text('Чтобы увидеть котика напиши /cat')


def echo(update):
    """Отвечаем ошибкой на любой текс"""
    update.message.reply_text("Ой, что-то не то :(")


def error(update):
    logger.warning('Update "%s" caused error "%s"', update, error)


def buy_cat():
    """Получаем ссылку на котика"""
    try:
        r = requests.get('http://thecatapi.com/api/images/get?format=src')
        url = r.url
    except IndexError:
        url = get_cat()
        print('Error with cat parsing')
        pass
    return url


def send_cat(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo=buy_cat(), reply_markup=draw_button())


def draw_button():
    keys = [[InlineKeyboardButton('Хочешь еще котика?', callback_data='1')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)


def get_callback_from_button(update, context):
    """Получаем котика"""
    query = update.callback_query
    chat_id = query.message.chat.id
    if int(query.data) == 1:
        context.bot.send_photo(photo=buy_cat(),
                               chat_id=chat_id,
                               reply_markup=draw_button())


def main():
    """Запускаем бот"""
    updater = Updater("1920392901:AAHLl79JjtNy2xWmKJfw1fc_IHaZJR41iI8")

    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(get_callback_from_button))
    dp.add_handler(CommandHandler("start", start, pass_args=True))
    dp.add_handler(CommandHandler("help", help_me))
    dp.add_handler(CommandHandler("cat", send_cat))
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
