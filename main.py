
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

GET_ID, GET_NAME, NAME_VALIDATION, SERVICE_LIST, GET_SERVICE, WAIT_PARENTHOOD = range(5)

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
    
def incorrectID(update, context):
    update.message.reply_text("baba dorost hesabi shomare daneshjuEto bezan dige, laelahaelalah")
    return GET_ID

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
        update.message.reply_text(getName, reply_markup=ReplyKeyboardRemove())
        return GET_NAME
    elif validation == 'hamine agha, berim':
        return SERVICE_LIST
    else:
        update.message.reply_text("emmm, yeki az gozine haro lotfan entekhab kon")
        return NAME_VALIDATION

def listServices(update, context):
    serviceIntro = """ service hayi ke mn be to {} aziz erae midam inas. Age barat jaleb bud, yekishun ro entekhab kon ta darbarash behet begam :)""".format("ESM_TO") 
    services = [['Yatim paziri']]
    update.message.reply_text(serviceIntro, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of service'
        ))
    return GET_SERVICE

def setService(update, context):
    service = update.message.text
    if service == 'Yatim paziri':
        global parenthood_message
        update.message.reply_text(parenthood_message, reply_markup=ReplyKeyboardRemove())
        options = [['❇sarparast mikham❇', 'Nah!']]
        update.message.reply_text("khob hala begu bebinam mikhai sarparast dashte bashi? ", ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='list of service'
        ))
        return WAIT_PARENTHOOD
    else: 
        services = [['Yatim paziri']]
        update.message.reply_text("Nadashtim hamchin serviceE ha🤔🤔, yebar dige entekhab kon", reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of service'
        ))
        return GET_SERVICE

def getParenthoodService(update, context):
    parenthood = update.message.text
    if parenthood=="❇sarparast mikham❇":
        update.message.reply_text("hale, be {} khabar midam ke biad be sarparasti ghabulet kone".format("STUDENT_ID_PARENT"), reply_markup=ReplyKeyboardRemove())
        return SERVICE_LIST
    elif parenthood == "Nah!":
        update.message.reply_text("eh chera? \nKhob ok harjur rahat tari, be {} khabar midam ke donbal ye bache dige bashe".format("STUDENT_ID_PARENT"), reply_markup=ReplyKeyboardRemove())
        return SERVICE_LIST
    else:
        update.message.reply_text("agha mn ke nafahmidam chi migi, az gozine ha yekio entekhab kon ya /skip bezan")
        return WAIT_PARENTHOOD

    

def noSkipGetId(update, context):
    update.message.reply_text("laelahaelalah, sare karie? ")
    return GET_ID

def noSkipGetName(update, context):
    update.message.reply_text("mage mishe mn esmet ro nadunam? noch noch, nemishe")
    return GET_NAME

def skipParenthood(update, context):
    update.message.reply_text("inghadr madar pedaret ro hers nade", reply_markup=ReplyKeyboardRemove())
    return SERVICE_LIST


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    update.message.reply_text("laelahaelalah, berim az aval pas", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("dobare shomare daneshjuEt ro vared kon.")
    return GET_ID


def main():
    global API_KEY
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_ID: [MessageHandler(Filters.regex('^40031.{3}'), setID), CommandHandler('skip', noSkipGetId), MessageHandler(Filters.text & ~Filters.command), incorrectID],
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, nameSet), CommandHandler('skip', noSkipGetName)],
            NAME_VALIDATION: [
                MessageHandler(Filters.text & ~Filters.command, nameValidation )
                # SERVICE_LIST, GET_SERVICE, WAIT_PARENTHOOD
            ],
            SERVICE_LIST:[MessageHandler(Filters.text & ~Filters.command, listServices)],
            GET_SERVICE:[MessageHandler(Filters.text & ~Filters.command, setService)],
            WAIT_PARENTHOOD:[ MessageHandler( Filters.text & ~Filters.command, getParenthoodService) , CommandHandler('skip', skipParenthood)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # to start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()