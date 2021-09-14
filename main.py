
import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from messages import * 


API_KEY = os.getenv('API_KEY')

# for logging in the host server, just in case ;) 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GET_ID, GET_NAME, NAME_VALIDATION = range(3)

def start(update, context):
    global start_message
    update.message.reply_text(start_message)
    nextStep = "Hala baraye inke shuru konim, shomare daneshjuEt ro vared kon."
    update.message.reply_text(nextStep)
    return GET_ID

def setID(update, context):
    # now we have the id, we must get the user's name
    studentId = update.message.text
    user = update.message.from_user
    logger.info("studentID of %s: %s", user.first_name, update.message.text)
    getName = "Lotfan esme va familit ro vared kon"
    update.message.reply_text(getName)
    return GET_NAME
    
def nameSet(update, context):
    name = update.message.text
    user = update.message.from_user
    logger.info("name of %s: %s", user.first_name, name)
    validation = "Aya in esm va familit hast?   "+str(name)
    reply_keyboard = [['talash dobare?', 'hamine agha, berim']]
    update.message.reply_text(validation, reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='name validation?'
        ))
    return NAME_VALIDATION


def nameValidation(update, context):
    validation = update.message.text
    if validation=='talash dobare?':
        getName = "pas Lotfan esm va familit ro vared kon"
        update.message.reply_text(getName)
        return GET_NAME
    elif validation == 'hamine agha, berim':
        return 


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    global API_KEY
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_ID: [MessageHandler(Filters.regex('^40031.{3}'), setID)],
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, nameSet)],
            NAME_VALIDATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # to start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()