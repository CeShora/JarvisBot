
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

import redis #to store the data
import json
from messages import * 


API_KEY = os.getenv('API_KEY')

# for logging in the host server, just in case ;) 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GET_ID, GET_NAME, NAME_VALIDATION, GET_SERVICE, WAIT_PARENTHOOD = range(5)

r = redis.Redis(host='localhost', port=6379, db=0)


def saveInfoToRedis(userId, chatId, keyString, valueString):
    saveInfo = None
    if r.get(userId)==None:
        saveInfo  = {}
        saveInfo["userId"] = userId
        saveInfo["chatId"] = chatId
        saveInfo[keyString] = valueString
    else:
        saveInfo = loadInfoFromRedis(userId)
        saveInfo[keyString]= valueString
    #now save data in redis database
    jsonDump = json.dumps(saveInfo)
    r.set(userId, jsonDump)
    r.save()

def loadInfoFromRedis(userId):
    saveInfo = json.loads(r.get(userId))
    return saveInfo

def start(update, context):

    #set up data about user
    saveInfoToRedis(str(update.message.from_user.id), str(update.message.chat_id), "username", str(update.message.from_user.username))

    global start_message
    update.message.reply_animation("CgACAgQAAxkBAAEMwmJhRH6My8SAhIuq5Jm6zDydoOKBXgACZAoAAojDKVI6bouBtlVi0SAE", caption=start_message) #sending the start.gif 
    nextStep = "Hala baraye inke shuru konim, shomare daneshjuEt ro vared kon."
    update.message.reply_text(nextStep, reply_markup=ReplyKeyboardRemove())
    return GET_ID

def setID(update, context):

    studentId = update.message.text
    user = update.message.from_user
    saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "studentID", studentId)

    logger.info("studentID of %s: %s", user.first_name, update.message.text)
    getName = "Lotfan esm va familit ro vared kon"
    update.message.reply_text(getName)
    return GET_NAME
    
def incorrectID(update, context):
    update.message.reply_text("baba dorost hesabi shomare daneshjuEto bezan dige, laelahaelalah")
    return GET_ID

def nameSet(update, context):
    name = update.message.text
    user = update.message.from_user
    
    saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "fullName", name)

    logger.info("name of %s: %s", user.first_name, name)
    validation = "Aya in esm va familit hast?   "+str(name)
    reply_keyboard = [['talash dobare?', 'hamine agha, berim']]
    update.message.reply_text(validation, reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='name validation?'
        ))
    return NAME_VALIDATION


def nameValidation(update, context):
    validation = update.message.text
    if validation == 'talash dobare?':
        getName = "pas Lotfan esm va familit ro vared kon"
        update.message.reply_text(getName, reply_markup=ReplyKeyboardRemove())
        return GET_NAME
    elif validation == 'hamine agha, berim':
        serviceIntro = """ service hayi ke mn erae midam inas. Age barat jaleb bud, yekishun ro entekhab kon ta darbarash behet begam :)"""
        services = [['Yatim paziri'],['Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
        update.message.reply_animation("CgACAgQAAxkBAAEMwmlhRH7fmq0UArijPx3gm30lrs-gsQACZQoAAojDKVKFb6w1HzVDDiAE", caption = serviceIntro, reply_markup = ReplyKeyboardMarkup(services))
        
        return GET_SERVICE
    else:
        update.message.reply_text("emmm, yeki az gozine haro lotfan entekhab kon")
        return NAME_VALIDATION

def setService(update, context):
    service = update.message.text
    if service == 'Yatim paziri':
        global parenthood_message
        update.message.reply_text(parenthood_message, reply_markup=ReplyKeyboardRemove())
        options = [['❇sarparast mikham❇', 'Nah!']]
        update.message.reply_text("khob hala begu bebinam mikhai sarparast dashte bashi? ", reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst service'
        ))
        return WAIT_PARENTHOOD
    elif service == 'Tashakol haye AUT va CE':
        global tashakolat_message
        services = [['Yatim paziri'],[ 'Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
        tashakolat_photo = open("gp.gif",'rb')
        update.message.reply_animation("CgACAgQAAxkBAAEMxSFhRPzRyInp5HdLxcOeP-pi4blrDgACHAsAAojDKVIrFauqcxMCaCAE", caption=tashakolat_message, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of services'
        ))
        return GET_SERVICE
    elif service == 'site haye AUT va CE':
        global sites_message
        services = [['Yatim paziri'],[ 'Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
        update.message.reply_animation("CgACAgQAAxkBAAEMwolhRIGd-LbyhG7VvahERfpct1NTOgACaQoAAojDKVICmTmOCfDM-yAE", caption=sites_message, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of services'
        ))
        return GET_SERVICE

    else: 
        services = [['Yatim paziri'],[ 'Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
        update.message.reply_text("Emmm... nadashtim hamchin serviceE ha🤔🤔, yebar dige entekhab kon", reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of service'
        ))
        return GET_SERVICE

def getParenthoodService(update, context):
    parenthood = update.message.text
    if parenthood=="❇sarparast mikham❇":
        
        #save in redis db
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "parentHood", True)

        update.message.reply_text("hale, be {} khabar midam ke biad be sarparasti ghabulet kone".format("STUDENT_ID_PARENT"), reply_markup=ReplyKeyboardRemove())
        nextService = "Dige che serviceE mikhai?"
        services = [['Yatim paziri'],[ 'Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
        update.message.reply_text(nextService, reply_markup = ReplyKeyboardMarkup(
                services, one_time_keyboard=True, input_field_placeholder='list of service'
            ))
        return GET_SERVICE
    elif parenthood == "Nah!":
        
        #save in redis db
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "parentHood", False)

        update.message.reply_text("eh chera? \nKhob ok harjur rahat tari, be {} khabar midam ke donbal ye bache dige bashe".format("STUDENT_ID_PARENT"), reply_markup=ReplyKeyboardRemove())
        nextService = "Dige che serviceE mikhai?"
        services = [['Yatim paziri'],[ 'Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
        update.message.reply_text(nextService, reply_markup = ReplyKeyboardMarkup(
                services, one_time_keyboard=True, input_field_placeholder='list of service'
            ))
        return GET_SERVICE
    else:
        update.message.reply_text("agha mn ke nafahmidam chi migi, az gozine ha yekio entekhab kon ya /skip bezan")
        return WAIT_PARENTHOOD

def noSkipGetId(update, context):
    update.message.reply_text("laelahaelalah, sare karie? ")
    return GET_ID

def noSkipGetName(update, context):
    update.message.reply_text("mage mishe mn esmet ro nadunam? noch noch, nemishe")
    return GET_NAME

def noSkipNameValidation(update, context):
    update.message.reply_text("laelahaelalah, agha ya esmet hast ya nist, in koli bazia dige chie?")
    return NAME_VALIDATION


def skipParenthood(update, context):
    update.message.reply_text("inghadr madar pedaret ro hers nade", reply_markup=ReplyKeyboardRemove())
    serviceIntro = """ hala service digeE mikhai?"""
    services = [['Yatim paziri'],[ 'Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
    update.message.reply_text(serviceIntro, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of service'
        ))
    return GET_SERVICE


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    update.message.reply_text("laelahaelalah, berim az aval pas", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("dobare shomare daneshjuEt ro vared kon.")
    return GET_ID

def idk_ServiceList(update, context):
    update.message.reply_text("chio mikhai skip koni khodaE alan?", reply_markup=ReplyKeyboardRemove())
    return None

def idk_command(update, context):
    update.message.reply_text("Emmm, hamchin commandE nadashtam ha!")
    return None

def skipService(update, context):
    update.message.reply_text("Chera inghadr ajale darE? alan mikhai koja beri? inja tahe khate...")
    return None


def main():
    global API_KEY
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_ID: [MessageHandler(Filters.regex('^40031.{3}'), setID), CommandHandler('skip', noSkipGetId), MessageHandler(Filters.text & ~Filters.command, incorrectID),  CommandHandler("start", start), MessageHandler(Filters.command, idk_command)],
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, nameSet), CommandHandler('skip', noSkipGetName), CommandHandler("start", start), MessageHandler(Filters.command, idk_command)],
            NAME_VALIDATION: [
                MessageHandler(Filters.text & ~Filters.command, nameValidation ), CommandHandler('skip', noSkipNameValidation), CommandHandler("start", start), MessageHandler(Filters.command, idk_command)
            ],
            GET_SERVICE:[MessageHandler(Filters.text & ~Filters.command, setService),  CommandHandler("skip", skipService), CommandHandler("start", start), MessageHandler(Filters.command, idk_command) ],
            WAIT_PARENTHOOD:[ MessageHandler( Filters.text & ~Filters.command, getParenthoodService) , CommandHandler('skip', skipParenthood), CommandHandler("start", start), MessageHandler(Filters.command, idk_command)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # to start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()