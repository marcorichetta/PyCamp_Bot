import logging
import sys
import os
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler, ConversationHandler)


from pycamp_bot import voting
from pycamp_bot import manage_pycamp
from pycamp_bot import projects
from pycamp_bot import wizard

from pycamp_bot.models import models_db_connection
from pycamp_bot.raffle import raffle
from pycamp_bot.help_msg import HELP_MESSAGE


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# command /start give user a message
def start(bot, update):
    logger.info('Start command')
    chat_id = update.message.chat_id

    if update.message.from_user.username is None:
        bot.send_message(
                chat_id=chat_id,
                text="""Hola! Necesitas tener un username primero.
                        \nCreate uno siguiendo esta guia: https://ewtnet.com/technology/how-to/how-to-add-a-username-on-telegram-android-app.
                        Y despues dame /start the nuevo :) """)

    elif update.message.from_user.username:
        bot.send_message(
                chat_id=chat_id,
                text='Hola ' + update.message.from_user.username + '! Bienvenidx')


def help(bot, update):
    logger.info('Returning help message')
    bot.send_message(chat_id=update.message.chat_id, text=HELP_MESSAGE)


def error(bot, update, error):
    '''Log Errors caused by Updates.'''
    logger.warning('Update {} caused error {}'.format(update, error))


def set_handlers(updater, dispatcher):
    # HANDLERS
    # handler that processes erros
    updater.dispatcher.add_error_handler(error)

    # Thread handlers

    dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('ayuda', help))
    wizard.set_handlers(updater)
    voting.set_handlers(updater)
    manage_pycamp.set_handlers(updater)
    projects.set_handlers(updater)

    updater.dispatcher.add_handler(CommandHandler('sorteo', raffle))


if __name__ == '__main__':
    logger.info('Starting PyCamp Bot')

    if 'TOKEN' in os.environ.keys():
        updater = Updater(token=os.environ['TOKEN'])
        dispatcher = updater.dispatcher

        users_status = {}
        current_projects = {}

        updater.start_polling()

        set_handlers(updater, dispatcher)
        models_db_connection(eval(sys.argv[1]))
    else:
        logger.info('Token not defined. Exiting.')
