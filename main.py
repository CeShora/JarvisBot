
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

import json
import re
from messages import * 
from adminUtils import *
from auth import *
from langUtils import *

API_KEY = os.getenv('API_KEY')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# for logging in the host server, just in case ;) 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LANG,  GET_ID, GET_NAME, NAME_VALIDATION, GET_SERVICE, WAIT_PARENTHOOD, GOD, GET_CHILD, GET_CHILD_NOT_PARENT, HALE= range(10)


FRESHMAN, SOPHOMORE, JUNIOR, SENIOR, IDK = range(5)

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
    """
    file = open("gifs/stork_baby.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/jarvis.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/gp.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/jarvis2.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/loading.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/site.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/site2.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/site3.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/site4.gif", "rb")
    update.message.reply_animation(file)
    file = open("gifs/start.gif", "rb")
    update.message.reply_animation(file)
    """
    # if its admin, then just take her(yes its gonna be me) to the "god" stage, lol, yes im a narcisist
    global ADMIN_CHAT_ID
    if str(update.message.chat_id) == ADMIN_CHAT_ID:
        update.message.reply_text("Hi admin👋", reply_markup=ReplyKeyboardRemove())
        logger.info("admin is talking to me :)")
        return GOD

    # set up data about user
    saveInfoToRedis(str(update.message.from_user.id), str(update.message.chat_id), "username", str(update.message.from_user.username))
    update.message.reply_text("پیامام چجوری باشه؟", reply_markup=ReplyKeyboardMarkup(
            [['Finglish', 'فارسی را پاس بداریم']], one_time_keyboard=True, input_field_placeholder='lang-set'
        ))
    return LANG


def setLang(update, context):
    lang = update.message.text
    
    start_message = '' 
    nextStep = ''

    if lang == 'فارسی را پاس بداریم':
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "lang", "fa")
        update.message.reply_text("حله", reply_markup=ReplyKeyboardRemove())
        start_message = start_message_FA
        nextStep = "حالا برای شروع شماره دانشجوییت رو وارد کن"
    elif lang == 'Finglish':
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "lang", "laelahaelalah")
        update.message.reply_text("bah bah, hale\nbezan berim", reply_markup=ReplyKeyboardRemove())
        start_message = start_message_LAELAHAELALAH
        nextStep = "Hala baraye inke shuru konim, shomare daneshjuEt ro vared kon."
    else:
        update.message.reply_text("من که نفهمیدم، بالاخره چی شد؟ پیامام چجوری باشه؟", reply_markup=ReplyKeyboardMarkup(
            [['Finglish', 'فارسی را پاس بداریم']], one_time_keyboard=True, input_field_placeholder='lang-set'
        ))
        return LANG
    #TODO in bayad bere baraye vurudia faghat
    update.message.reply_animation("CgACAgQAAxkBAAEM6ddhTD7uP4tsRiWKaVaw6dmLopTblQACrQwAAmxWYVJ9UMrHXsSt9yEE", caption=start_message) #sending the start.gif 
    update.message.reply_text(nextStep, reply_markup=ReplyKeyboardRemove())
    return GET_ID

def setID(update, context):
    studentId = update.message.text
    user = update.message.from_user
    saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "studentID", studentId)

    logger.info("studentID of %s: %s", user.first_name, update.message.text)


    lang = getStyle(update.message.from_user.id)
    getName = ''
    if lang == None:
        update.message.reply_text("من که نفهمیدم، بالاخره چی شد؟ پیامام چجوری باشه؟", reply_markup=ReplyKeyboardMarkup(
            [['Finglish', 'فارسی را پاس بداریم']], one_time_keyboard=True, input_field_placeholder='lang-set'
        ))
        return LANG
    elif lang == FA:
        getName = "لطفا اسم و فامیلیت رو وارد کن"
    elif lang == LAELAHAELALAH:
        getName = "Lotfan esm va familit ro vared kon"

    update.message.reply_text(getName)
    return GET_NAME
    
    
def incorrectID(update, context):
    lang = getStyle(update.message.from_user.id)
    correctInput = ''
    if lang == None:
        update.message.reply_text("من که نفهمیدم، بالاخره چی شد؟ پیامام چجوری باشه؟", reply_markup=ReplyKeyboardMarkup(
            [['Finglish', 'فارسی را پاس بداریم']], one_time_keyboard=True, input_field_placeholder='lang-set'
        ))
        return LANG
    elif lang == FA:
        correctInput = "لطفا  شماره دانشجوایت رو وارد کن"
    elif lang == LAELAHAELALAH:
        correctInput = "baba dorost hesabi shomare daneshjuEto bezan dige, laelahaelalah"
    update.message.reply_text(correctInput)
    return GET_ID

def nameSet(update, context):
    name = update.message.text
    user = update.message.from_user
    
    saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "fullName", name)
    logger.info("name of %s: %s", user.first_name, name)

    lang = getStyle(update.message.from_user.id)
    validation = ''
    reply_keyboard = [['talash dobare?', 'hamine agha, berim']]
    if lang == None:
        update.message.reply_text("من که نفهمیدم، بالاخره چی شد؟ پیامام چجوری باشه؟", reply_markup=ReplyKeyboardMarkup(
            [['Finglish', 'فارسی را پاس بداریم']], one_time_keyboard=True, input_field_placeholder='lang-set'
        ))
        return LANG
    elif lang == FA:
        validation = "آیا اسم و فامیلیت همینه؟"+str(name)
        reply_keyboard = [['تلاش دوباره', 'درست']]
    elif lang == LAELAHAELALAH:
        validation = "Aya in esm va familit hast?   "+str(name)
        reply_keyboard = [['talash dobare?', 'hamine agha, berim']]

    
    update.message.reply_text(validation, reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='name validation?'
        ))
    return NAME_VALIDATION

def studentState(userId):
    userData = loadInfoFromRedis(userId)
    try:
        studentId = userData["studentID"]
    except KeyError:
        return IDK
    if re.search("(^40031.{3}$)", studentId):
        return FRESHMAN
    elif re.search("(^9931.{3}$)", studentId):
        return SOPHOMORE
    elif re.search("(^9831.{3}$)", studentId):
        return JUNIOR
    elif re.search("(^9731.{3}$)", studentId):
        return SENIOR
    else:
        return IDK


def nameValidation(update, context):
    validation = update.message.text
    studentState_ = studentState(update.message.from_user.id)
    if studentState_ == IDK:
        start_ = start()
        return start_
    elif studentState_ == FRESHMAN:
        if validation == 'talash dobare?':
            getName = "pas Lotfan esm va familit ro vared kon"
            update.message.reply_text(getName, reply_markup=ReplyKeyboardRemove())
            return GET_NAME
        elif validation == 'hamine agha, berim':

            ########################### NOTIFY ADMIN ###########################
            global ADMIN_CHAT_ID
            notifyAdmin(ADMIN_CHAT_ID, r, context)
            ############################### DONE ###############################
            
            serviceIntro = """ service hayi ke mn erae midam inas. Age barat jaleb bud, yekishun ro entekhab kon ta darbarash behet begam :)"""
            services = [['Yatim paziri'],['Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
            update.message.reply_animation("CgACAgQAAxkBAAEM6fthTEDkB3_D6pNLofIygH7TfqD-jwACqAwAAmxWYVJY0KkLyzDA5CEE", #loading gif
             caption = serviceIntro, reply_markup = ReplyKeyboardMarkup(services))
            
            return GET_SERVICE
        else:
            update.message.reply_text("emmm, yeki az gozine haro lotfan entekhab kon")
            return NAME_VALIDATION
    elif studentState_ == SOPHOMORE:
        options = getOptions
        # stork = open("gifs/stork_baby.gif", 'rb')
        update.message.reply_animation("CgACAgQAAxkBAAEM6kFhTEVeaezEOF7Z1J7v3yagXy5hGAACagoAAmxWaVJBWswaHL8d0iEE")
        grandChildText = getGrandChildText()
        update.message.reply_text("bah bah, umadi bache tahvil begiri?", reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst service'
        ))
        return GET_CHILD
    elif studentState_ == JUNIOR  :
        # stork = open("gifs/stork_baby.gif", 'rb')
        update.message.reply_animation("CgACAgQAAxkBAAEM6kFhTEVeaezEOF7Z1J7v3yagXy5hGAACagoAAmxWaVJBWswaHL8d0iEE")
        options = [['Re, lets go!', 'Nop']]
        update.message.reply_text("bah bah, umadi nave tahvil begiri?", reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst child'
        ))
        return GET_CHILD_NOT_PARENT
    elif studentState_ == SENIOR  :
        # stork = open("gifs/stork_baby.gif", 'rb')
        update.message.reply_animation("CgACAgQAAxkBAAEM6kFhTEVeaezEOF7Z1J7v3yagXy5hGAACagoAAmxWaVJBWswaHL8d0iEE")
        options = [['Re, lets go!', 'Nop']]
        update.message.reply_text("bah bah, umadi nabire tahvil begiri?", reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst child'
        ))
        return GET_CHILD_NOT_PARENT


def getChildNotParent(update, context):
    child = update.message.text
    if child =='Re, lets go!':
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text("hale, behesh khabar midim age madar pedar nadasht biad pish to", reply_markup = ReplyKeyboardRemove())
    elif child == 'Nop':
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text("ishala ke bachat masuliat pazire", reply_markup = ReplyKeyboardRemove())
    else:
        update.message.reply_text("durugh chera nafahmidam chi gofT, dobare vared kon", reply_markup = ReplyKeyboardRemove())
        options = [['Re, lets go!', 'Nop']]
        update.message.reply_text("bah bah, umadi nabire tahvil begiri?", reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst child'
        ))
        return GET_CHILD_NOT_PARENT
    return HALE


def getChild(update, context):
    child = update.message.text
    if child =='Re, lets go!':
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text("hale, behesh khabar midim ke biad dar aghush khanevade", reply_markup = ReplyKeyboardRemove())
    elif child == 'Nop':
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text("hale, behesh khabar midim bere ye sarparast peida kone", reply_markup = ReplyKeyboardRemove())
    else:
        update.message.reply_text("durugh chera nafahmidam chi gofT, dobare vared kon", reply_markup = ReplyKeyboardRemove())
        options = [['Re, lets go!', 'Nop']]
        update.message.reply_text("bah bah, umadi bache tahvil begiri?", reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst service'
        ))
        return GET_CHILD
    return HALE

def hale(update, context):
    update.message.reply_text("hale dige, hamahagi haye lazem ro mikonam va age khabari bud behet midam")
    return None

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
        update.message.reply_animation("CgACAgQAAxkBAAEM6glhTEGXueA6zdL910ZLEO7tAlxtUAACpgwAAmxWYVJp-BJS4aRtjyEE", #gp.gif
         caption=tashakolat_message, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of services'
        ))
        return GET_SERVICE
    elif service == 'site haye AUT va CE':
        global sites_message
        services = [['Yatim paziri'],[ 'Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
        update.message.reply_animation("CgACAgQAAxkBAAEM6g1hTEHTW1IEYRvheVszhp3Eyy_3IwACrAwAAmxWYVJH4AtOkexidyEE", caption=sites_message, reply_markup = ReplyKeyboardMarkup(
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
            LANG: [MessageHandler( Filters.text & ~Filters.command , setLang)],
            GET_ID: [MessageHandler(Filters.regex('^40031.{3}'), setID), MessageHandler(Filters.regex('^9931.{3}'), setID), MessageHandler(Filters.regex('^9831.{3}'), setID) , MessageHandler(Filters.regex('^9731.{3}'), setID), CommandHandler('skip', noSkipGetId), MessageHandler(Filters.text & ~Filters.command, incorrectID),  CommandHandler("start", start), MessageHandler(Filters.command, idk_command)],
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, nameSet), CommandHandler('skip', noSkipGetName), CommandHandler("start", start), MessageHandler(Filters.command, idk_command)],
            NAME_VALIDATION: [
                MessageHandler(Filters.text & ~Filters.command, nameValidation ), CommandHandler('skip', noSkipNameValidation), CommandHandler("start", start), MessageHandler(Filters.command, idk_command)
            ],
            GET_SERVICE:[MessageHandler(Filters.text & ~Filters.command, setService),  CommandHandler("skip", skipService), CommandHandler("start", start), MessageHandler(Filters.command, idk_command) ],
            WAIT_PARENTHOOD:[ MessageHandler( Filters.text & ~Filters.command, getParenthoodService) , CommandHandler('skip', skipParenthood), CommandHandler("start", start), MessageHandler(Filters.command, idk_command)],
            GOD: [CommandHandler("data", admin), MessageHandler(Filters.regex('^40031.{3}'), getData),MessageHandler(Filters.regex('^9931.{3}'), getData), MessageHandler(Filters.regex('^9831.{3}'), getData),MessageHandler(Filters.regex('^9731.{3}'), getData), MessageHandler(Filters.all, imDumb)],
            GET_CHILD: [ MessageHandler( Filters.text & ~Filters.command, getChild), CommandHandler("start", start)],
            HALE:[MessageHandler(Filters.all & ~Filters.command, hale), CommandHandler("start", start)],
            GET_CHILD_NOT_PARENT:[MessageHandler(Filters.all & ~Filters.command, getChildNotParent), CommandHandler("start", start)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # to start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()