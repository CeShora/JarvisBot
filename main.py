
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

LANG,  GET_ID, GET_NAME, NAME_VALIDATION, GET_SERVICE, WAIT_PARENTHOOD, GOD, GET_CHILD, GET_CHILD_NOT_PARENT, HALE, NOT_AUTH= range(11)


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

    if not isAuth():
        update.message.reply_text(getNotAuth(), reply_markup=ReplyKeyboardRemove())
        return NOT_AUTH

    # set up data about user
    user = update.message.from_user.username
    saveInfoToRedis(str(update.message.from_user.id), str(update.message.chat_id), "username", str(user['username']))
    options = getLangOpt()
    update.message.reply_text(getLang(), reply_markup=ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lang-set'
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
        update.message.reply_text(idGetIt(), reply_markup=ReplyKeyboardMarkup(
            getLangOpt(), one_time_keyboard=True, input_field_placeholder='lang-set'
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
    if lang == None:
        update.message.reply_text(idGetIt(), reply_markup = ReplyKeyboardMarkup(
            getLangOpt(), one_time_keyboard=True, input_field_placeholder='lang-set'
        ))
        return LANG
        
    getName_ = getName(update.message.from_user.id)
    update.message.reply_text(getName_)
    return GET_NAME

def incorrectID(update, context):
    lang = getStyle(update.message.from_user.id)
    correctInput = ''
    if lang == None:
        update.message.reply_text(idGetIt(), reply_markup=ReplyKeyboardMarkup(
            getLangOpt(), one_time_keyboard=True, input_field_placeholder='lang-set'
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
        update.message.reply_text(idGetIt(), reply_markup=ReplyKeyboardMarkup(
            getLangOpt(), one_time_keyboard=True, input_field_placeholder='lang-set'
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
    global ADMIN_CHAT_ID
    validation = update.message.text
    userId =update.message.from_user.id
    studentState_ = studentState(userId)

    if studentState_ == IDK:
        start_ = start(update, context)
        return start_
    elif studentState_ == FRESHMAN:
        if validation == 'talash dobare?' or validation == 'تلاش دوباره?' :
            getName = getNameAgain(userId)
            update.message.reply_text(getName, reply_markup=ReplyKeyboardRemove())
            return GET_NAME
        elif validation == 'hamine agha, berim' or validation == "درست":

            ########################### NOTIFY ADMIN ###########################
            notifyAdmin(ADMIN_CHAT_ID, r, context)
            ############################### DONE ###############################
            
            serviceIntro = getServiceIntro(userId)
            services = getServiceOptions(userId)
            update.message.reply_animation("CgACAgQAAxkBAAEM6fthTEDkB3_D6pNLofIygH7TfqD-jwACqAwAAmxWYVJY0KkLyzDA5CEE", #loading gif
             caption = serviceIntro, reply_markup = ReplyKeyboardMarkup(services))
            
            return GET_SERVICE
        else:
            update.message.reply_text(getChoseOneOption(userId))
            return NAME_VALIDATION
    elif studentState_ == SOPHOMORE:
        if validation == 'talash dobare?' or validation == 'تلاش دوباره?' :
            getName = getNameAgain(userId)
            update.message.reply_text(getName, reply_markup=ReplyKeyboardRemove())
            return GET_NAME
        elif validation == 'hamine agha, berim' or validation == "درست":

            ########################### NOTIFY ADMIN ###########################
            notifyAdmin(ADMIN_CHAT_ID, r, context)
            ############################### DONE ###############################
            
            # stork = open("gifs/stork_baby.gif", 'rb')
            update.message.reply_animation("CgACAgQAAxkBAAEM6kFhTEVeaezEOF7Z1J7v3yagXy5hGAACagoAAmxWaVJBWswaHL8d0iEE")
            options = getOptions(userId)
            update.message.reply_text(getChildText(userId), reply_markup = ReplyKeyboardMarkup(
                options, one_time_keyboard=True, input_field_placeholder='lst child'
            ))
            return GET_CHILD
        else:
            update.message.reply_text(getNameAgain(userId) , reply_markup=ReplyKeyboardRemove())
            return GET_NAME
    elif studentState_ == JUNIOR  :
        if validation == 'talash dobare?' or validation == 'تلاش دوباره?' :
            getName = getNameAgain(userId)
            update.message.reply_text(getName, reply_markup=ReplyKeyboardRemove())
            return GET_NAME
        elif validation == 'hamine agha, berim' or validation == "درست":

            ########################### NOTIFY ADMIN ###########################
            notifyAdmin(ADMIN_CHAT_ID, r, context)
            ############################### DONE ###############################
            
            # stork = open("gifs/stork_baby.gif", 'rb')
            update.message.reply_animation("CgACAgQAAxkBAAEM6kFhTEVeaezEOF7Z1J7v3yagXy5hGAACagoAAmxWaVJBWswaHL8d0iEE")
            options = getOptions(userId)
            update.message.reply_text(getGrandChildText(userId), reply_markup = ReplyKeyboardMarkup(
                options, one_time_keyboard=True, input_field_placeholder='lst child'
            ))
            return GET_CHILD_NOT_PARENT
        else:
            update.message.reply_text(getNameAgain(userId) , reply_markup=ReplyKeyboardRemove())
            return GET_NAME
    elif studentState_ == SENIOR  :

        if validation == 'talash dobare?' or validation == 'تلاش دوباره?' :
            getName = getNameAgain(userId)
            update.message.reply_text(getName, reply_markup=ReplyKeyboardRemove())
            return GET_NAME
        elif validation == 'hamine agha, berim' or validation == "درست":

            ########################### NOTIFY ADMIN ###########################
            notifyAdmin(ADMIN_CHAT_ID, r, context)
            ############################### DONE ###############################
            
            # stork = open("gifs/stork_baby.gif", 'rb')
            update.message.reply_animation("CgACAgQAAxkBAAEM6kFhTEVeaezEOF7Z1J7v3yagXy5hGAACagoAAmxWaVJBWswaHL8d0iEE")
            options = getOptions(userId)
            update.message.reply_text(getGrandGrandChild(userId), reply_markup = ReplyKeyboardMarkup(
                options, one_time_keyboard=True, input_field_placeholder='lst child'
            ))
            return GET_CHILD_NOT_PARENT
        else:
            update.message.reply_text(getNameAgain(userId) , reply_markup=ReplyKeyboardRemove())
            return GET_NAME



def getChildNotParent(update, context):
    child = update.message.text
    userId = update.message.from_user.id
    if child =='Re, lets go!' or child == "بله":
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text(getNotificationForNotParent(userId), reply_markup = ReplyKeyboardRemove())
    elif child == 'Nop' or child == "خیر":
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text(getHopeResponsibleChild(userId), reply_markup = ReplyKeyboardRemove())
    else:
        update.message.reply_text(getDidNotUnderstand(userId), reply_markup = ReplyKeyboardRemove())
        options = getOptions(userId)
        update.message.reply_text(getWhyHere(userId), reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst child'
        ))
        return GET_CHILD_NOT_PARENT
    return HALE


def getChild(update, context):
    child = update.message.text
    userId = update.message.from_user.id
    if child =='Re, lets go!' or child == "بله":
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text(getNotifyMyChild(userId), reply_markup = ReplyKeyboardRemove())
    elif child == 'Nop' or child == "خیر":
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "WantsChild", True)
        update.message.reply_text(getNotifUnwantedChild(userId), reply_markup = ReplyKeyboardRemove())
    else:
        update.message.reply_text(getDidNotUnderstand(userId), reply_markup = ReplyKeyboardRemove())
        options = getOptions(userId)
        update.message.reply_text( getChildText(userId), reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst service'
        ))
        return GET_CHILD
    return HALE

def hale(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getWillOrganize(userId))
    return None

def setService(update, context):
    service = update.message.text
    userId = update.message.from_user.id
    if service == 'Parent yabi' or service=='پیدا کردن پدر و مادر':
        parenthood_message = getParenthood_message(userId)
        update.message.reply_text(parenthood_message, reply_markup=ReplyKeyboardRemove())
        options = getParentOption(userId)
        update.message.reply_text(getWillToHaveParent(userId), reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True, input_field_placeholder='lst service'
        ))
        return WAIT_PARENTHOOD
    elif service == 'Tashakol haye AUT va CE' or service =="تشکل های دانشگاه و دانشکده":
        tashakolat_message = getTashakolatMessage(userId)
        services = getServiceOptions(userId)
        update.message.reply_animation("CgACAgQAAxkBAAEM6glhTEGXueA6zdL910ZLEO7tAlxtUAACpgwAAmxWYVJp-BJS4aRtjyEE", #gp.gif
         caption=tashakolat_message, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of services'
        ))
        return GET_SERVICE
    elif service == 'site haye AUT va CE' or service == 'سایت های دانشگاه و دانشکده':
        sites_message = getSitesMessage(userId)
        services = getServiceOptions(userId)
        update.message.reply_animation("CgACAgQAAxkBAAEM6g1hTEHTW1IEYRvheVszhp3Eyy_3IwACrAwAAmxWYVJH4AtOkexidyEE", caption=sites_message, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of services'
        ))
        return GET_SERVICE

    else: 
        services = getServiceOptions(userId)
        update.message.reply_text(weDontHaveThatHereStopDoingCrack(userId), reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of service'
        ))
        return GET_SERVICE

def getParenthoodService(update, context):
    userId = update.message.from_user.id
    parenthood = update.message.text
    if parenthood=="❇sarparast mikham❇" or parenthood=='❇سرپرست میخوام❇':
        #save in redis db
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "parentHood", True)
        studentId = loadInfoFromRedis(update.message.from_user.id)
        studentId = studentId["studentID"]
        update.message.reply_text(getNotifyMyParent(userId=userId, studentId=studentId), reply_markup=ReplyKeyboardRemove())
        nextService = getAnyOtherService(userId)
        services = getServiceOptions(userId)
        update.message.reply_text(nextService, reply_markup = ReplyKeyboardMarkup(
                services, one_time_keyboard=True, input_field_placeholder='list of service'
            ))
        return GET_SERVICE
    elif parenthood == "Nah!" or parenthood =='نه':
        
        #save in redis db
        saveInfoToRedis(update.message.from_user.id, update.message.chat_id, "parentHood", False)

        studentId = loadInfoFromRedis(update.message.from_user.id)
        studentId = studentId["studentID"]

        update.message.reply_text(dontWantParent(userId, studentId), reply_markup=ReplyKeyboardRemove())
        nextService = getAnyOtherService(userId)
        services = getServiceOptions(userId)
        update.message.reply_text(nextService, reply_markup = ReplyKeyboardMarkup(
                services, one_time_keyboard=True, input_field_placeholder='list of service'
            ))
        return GET_SERVICE
    else:
        update.message.reply_text(getIdkWaitingParenthood(userId))
        return WAIT_PARENTHOOD

def noSkipGetId(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getLaelahaelalah(userId))
    return GET_ID

def noSkipGetName(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getCantBe(userId))
    return GET_NAME

def noSkipNameValidation(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getKoliBazi(userId=userId))
    return NAME_VALIDATION

def skipParenthood(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getBadChild(userId), reply_markup=ReplyKeyboardRemove())
    serviceIntro = getAnotherService(userId)
    services = getServiceOptions(userId)
    update.message.reply_text(serviceIntro, reply_markup = ReplyKeyboardMarkup(
            services, one_time_keyboard=True, input_field_placeholder='list of service'
        ))
    return GET_SERVICE


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getCanceledMidway(userId), reply_markup=ReplyKeyboardRemove())
    return GET_ID

def idk_ServiceList(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getIdkMan(userId), reply_markup=ReplyKeyboardRemove())
    return None

def idk_command(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getStudentDoingCrack(userId))
    return None

def skipService(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getNoSkip(userId))
    return None

def cannotCancel(update, context):
    userId = update.message.from_user.id
    update.message.reply_text(getDoNotcancel(userId))

def notAuth(update, context):
    update.message.reply_text(getNotAuth(), reply_markup=ReplyKeyboardRemove())


def main():
    global API_KEY
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG: [MessageHandler( Filters.text & ~Filters.command , setLang)],

            GET_ID: [MessageHandler(Filters.regex('^40031.{3}'), setID), MessageHandler(Filters.regex('^9931.{3}'), setID), MessageHandler(Filters.regex('^9831.{3}'), setID) ,
            MessageHandler(Filters.regex('^9731.{3}'), setID), CommandHandler('skip', noSkipGetId) , MessageHandler(Filters.text & ~Filters.command, incorrectID),
            CommandHandler("start", start), CommandHandler("cancel", cannotCancel), MessageHandler(Filters.command, idk_command)],
            
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, nameSet), CommandHandler('skip', noSkipGetName), CommandHandler("start", start), CommandHandler("cancel", cannotCancel), MessageHandler(Filters.command, idk_command)],
            
            NAME_VALIDATION: [
                MessageHandler(Filters.text & ~Filters.command, nameValidation ), CommandHandler('skip', noSkipNameValidation), CommandHandler("start", start), CommandHandler("cancel", cannotCancel), MessageHandler(Filters.command, idk_command)
            ],
            
            GET_SERVICE:[MessageHandler(Filters.text & ~Filters.command, setService),  CommandHandler("skip", skipService), CommandHandler("start", start), MessageHandler(Filters.command, idk_command) ],
            
            WAIT_PARENTHOOD:[ MessageHandler( Filters.text & ~Filters.command, getParenthoodService) , CommandHandler('skip', skipParenthood), CommandHandler('cancel', skipParenthood), CommandHandler("start", start), MessageHandler(Filters.command, idk_command)],
            
            GOD: [CommandHandler("data", admin), MessageHandler(Filters.regex('^40031.{3}'), getData),MessageHandler(Filters.regex('^9931.{3}'), getData), MessageHandler(Filters.regex('^9831.{3}'), getData),MessageHandler(Filters.regex('^9731.{3}'), getData), MessageHandler(Filters.all, imDumb)],
            
            GET_CHILD: [ MessageHandler( Filters.text & ~Filters.command, getChild), CommandHandler("start", start)],
            
            HALE:[MessageHandler(Filters.all & ~Filters.command, hale), CommandHandler("start", start)],
            
            GET_CHILD_NOT_PARENT:[MessageHandler(Filters.all & ~Filters.command, getChildNotParent), CommandHandler("start", start), CommandHandler("skip", skipService)],
            NOT_AUTH : [MessageHandler(Filters.all, notAuth)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # to start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()