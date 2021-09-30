
import redis
import json
from messages import * 
import re

r = redis.Redis(host='localhost', port=6379, db=0)


FA, LAELAHAELALAH = range(2)

def getStyle(userId):
    saveInfo = json.loads(r.get(userId))
    lang = saveInfo['lang']
    if lang is None:
        return None
    elif lang == 'fa':
        return FA
    elif lang == "laelahaelalah":
        return LAELAHAELALAH
    return None



def getLang():
    return "پیامام چجوری باشه؟"

def getLangOpt():
    return [['Finglish', 'فارسی را پاس بداریم']]

# def getPleaseEnterName

def getOptions(userId):
    options = [['Re, lets go!', 'Nop']]
    if getStyle(userId)==FA:
        options = [['بله', 'خیر']]
        return options
    elif getStyle(userId)==LAELAHAELALAH:
        return options

def getGrandChildText(userId):
    grandChildText = "bah bah, umadi nave tahvil begiri?"
    if getStyle(userId)==FA:
        grandChildText = "به به اومدی نوه تحویل بگیری؟"
        return grandChildText
    elif getStyle(userId)==LAELAHAELALAH:
        return grandChildText

def getChildText(userId):
    childText = "bah bah, umadi bache tahvil begiri?"
    if getStyle(userId)==FA:
        childText = "به به اومدی بچه تحویل بگیری؟"
        return childText
    elif getStyle(userId)==LAELAHAELALAH:
        return childText
        
def getGrandGrandChild(userId):
    grandGrandChildText = "bah bah, umadi nabire tahvil begiri?"
    if getStyle(userId)==FA:
        grandGrandChildText = "به به اومدی نبیره تحویل بگیری؟"
        return grandGrandChildText
    elif getStyle(userId)==LAELAHAELALAH:
        return grandGrandChildText


def getWhyHere(userId):
    message = "belakhare umadi 400E tahvil begiri ya na?"
    if getStyle(userId)==FA:
        message = "بالاخره چی شد؟"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getNameAgain(userId):
    getName = "pas Lotfan esm va familit ro vared kon"
    if getStyle(userId)==FA:
        getName = "دوباره وارد کن اسم و فامیلیت رو"
        return getName
    elif getStyle(userId)==LAELAHAELALAH:
        return getName

def getServiceIntro(userId):
    serviceIntro = """ service hayi ke mn erae midam inas. Age barat jaleb bud, yekishun ro entekhab kon ta darbarash behet begam :)"""
    if getStyle(userId)==FA:
        serviceIntro = """این کاراییه که من میتونم انجام بدم. یکیشون رو انتخاب کن تا با هم شروع کنیم"""
        return serviceIntro
    elif getStyle(userId)==LAELAHAELALAH:
        return serviceIntro

def getServiceOptions(userId):
    services = [['Parent yabi'],['Tashakol haye AUT va CE', 'site haye AUT va CE' ]]
    if getStyle(userId)==FA:
        services =  [['پیدا کردن پدر و مادر'],['تشکل های دانشگاه و دانشکده', 'سایت های دانشگاه و دانشکده' ]]
        return services
    elif getStyle(userId)==LAELAHAELALAH:
        return services

def getChoseOneOption(userId):
    chooseOneOpt = "emmm, yeki az gozine haro lotfan entekhab kon"
    if getStyle(userId)==FA:
        chooseOneOpt = "یکی از گزینه ها رو انتخاب کن لطفا"
        return chooseOneOpt
    elif getStyle(userId)==LAELAHAELALAH:
        return chooseOneOpt

def getNotifyMyChild(userId):
    notifi = "hale, behesh khabar midim ke biad dar aghush khanevade"
    if getStyle(userId)==FA:
        notifi = "اکی، بهش خبر میدیم"
        return notifi
    elif getStyle(userId)==LAELAHAELALAH:
        return notifi

def getNotifUnwantedChild(userId):
    notifi = "hale, behesh khabar midim bere ye sarparast peida kone"
    if getStyle(userId)==FA:
        notifi = "اکی، بهش خبر میدیم "
        return notifi
    elif getStyle(userId)==LAELAHAELALAH:
        return notifi

def getDidNotUnderstand(userId):
    message = "durugh chera nafahmidam chi gofT, dobare vared kon"
    if getStyle(userId)==FA:
        message = "نفهمیدم، دوباره وارد کن "
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getNotificationForNotParent(userId):
    message = "hale, behesh khabar midim age madar pedar nadasht biad pish to"
    if getStyle(userId)==FA:
        message = "بهش خبر میدیم اگر سرپرست نداشت بیاد پیش تو"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getHopeResponsibleChild(userId):
    message = "ishala ke bachat masuliat pazire chon az to ke abi garm nemishe"
    if getStyle(userId)==FA:
        message = "ایشالا که بچت مسولیت پذیره"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getWillOrganize(userId):
    message = "hale dige, hamahangi haye lazem ro mikonam va age khabari bud behet midam"
    if getStyle(userId)==FA:
        message = "اکی، من هماهنگی های لازم رو میکنم خبر میدم بهت"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getParenthood_message(userId):
    parenthood_message = parenthood_message_LAELAHAELALAH
    if getStyle(userId)==FA:
        parenthood_message =parenthood_message_FA
        return parenthood_message
    elif getStyle(userId)==LAELAHAELALAH:
        return parenthood_message

def getParentOption(userId):
    options = [['❇sarparast mikham❇', 'Nah!']]
    if getStyle(userId)==FA:
        options = [['❇سرپرست میخوام❇','نه']]
        return options 
    elif getStyle(userId)==LAELAHAELALAH:
        return options 

def getWillToHaveParent(userId):
    message = "khob hala begu bebinam mikhai sarparast dashte bashi?"
    if getStyle(userId)==FA:
        message = "خب حالا بگو ببینم میخوای مامان یا بابا داشته باشی؟"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getTashakolatMessage(userId):
    tashakolat_message = tashakolat_message_LAELAHAELALAH
    if getStyle(userId)==FA:
        tashakolat_message = tashakolat_message_FA
        return tashakolat_message
    elif getStyle(userId)==LAELAHAELALAH:
        return tashakolat_message

def getSitesMessage(userId):
    sitesMessage = sites_message_LAELAHAELALAH
    if getStyle(userId)==FA:
        sitesMessage = sites_message_FA
        return sitesMessage
    elif getStyle(userId)==LAELAHAELALAH:
        return sitesMessage

def weDontHaveThatHereStopDoingCrack(userId):
    message = "Emmm... nadashtim hamchin serviceE ha🤔🤔, shoma be nazaram  parket ro avaz kon va badesh bia yebar dige entekhab kon"
    if getStyle(userId)==FA:
        message = "نداشتیم همچین چیزیا! یه بار دیگه انتخاب کن"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getParentId(studentId):
    if re.search("(^40031.{3}$)", studentId):
        return(str(99)+studentId[3:])
        
def getNotifyMyParent(userId, studentId):
    message = "hale, be {} khabar midam ke biad be sarparasti ghabulet kone".format(getParentId(studentId))
    if getStyle(userId)==FA:
        message = "حله الان به" + getParentId(studentId) + "خبر میدم که بیاد سرپرستیت رو به عده بگیره😁"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getAnyOtherService(userId):
    message = "Dige che serviceE mikhai?"
    if getStyle(userId)==FA:
        message = "دیگه چه سرویسی میخوای؟"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def dontWantParent(userId, studentId):
    reply = "eh chera? \nKhob ok harjur rahat tari, be {} khabar midam ke donbal ye bache dige bashe".format(getParentId(studentId))
    if getStyle(userId)==FA:
        message = "باشه هرجور راحت تری. به "+getParentId(studentId)+"خبر میدیم که دنبال یه بچه دیگه باشه"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getIdkWaitingParenthood(userId):
    message = "agha mn ke nafahmidam chi migi, az gozine ha yekio entekhab kon ya /skip bezan"
    if getStyle(userId)==FA:
        message = "نفهمیدم، دوباره وارد کن یا /skip بزن"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getLaelahaelalah(userId):
    message = "laelahaelalah, sare karie? "
    if getStyle(userId)==FA:
        message = "laelahaelalah، سره کاریه؟"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getCantBe(userId):
    message = "mage mishe mn esmet ro nadunam? noch noch, nemishe"
    if getStyle(userId)==FA:
        message = "من باید اسمت رو بدونم، لطفا واردش کن"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getKoliBazi(userId):
    message = "laelahaelalah, agha ya esmet hast ya nist, in koli bazia dige chie?"
    if getStyle(userId)==FA:
        message = "laelahaelalah، این کلی بازیا چیه یا اسمت هست یا نیست دیگه"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getAnotherService(userId):
    message = """ hala service che digeE mikhai?"""
    if getStyle(userId)==FA:
        message = "خب حالا چه سرویس دیگه ای میخوای؟"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getBadChild(userId):
    message = "inghadr madar pedaret ro hers nade"
    if getStyle(userId)==FA:
        message = "اینقدر مادر/پدرت رو اذیت نکن"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getIdkMan(userId):
    message = "chio mikhai skip koni khodaE alan?"
    if getStyle(userId)==FA:
        message = "الان چیو میخوای اسکیپ کنی خدایی؟"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getStudentDoingCrack(userId):
    message = "Emmm, hamchin commandE nadashtam ha!"
    if getStyle(userId)==FA:
        message = "نداشتیم همچین کامندی"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getNoSkip(userId):
    message = "Chera inghadr ajale darE? alan mikhai koja beri? inja tahe khate..."
    if getStyle(userId)==FA:
        message = "چیو میخوای اسکیپ کنی؟ اینجا دیگه ته خطه"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getDoNotcancel(userId):
    message = "inja nemishe cancel kard"
    if getStyle(userId)==FA:
        message = "اینجا نمیشه کنسل کرد"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getPleaseChooseOneOftheOptions(userId):
    message = "amu yeki az gozine haro entekhab kon"
    if getStyle(userId)==FA:
        message = "یکی از گزینه ها رو انتخاب کنید"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message
        
def getName(userId):
    message = "Lotfan esm va familit ro vared kon"
    if getStyle(userId)==FA:
        message = "لطفا اسم و فامیلیت رو وارد کن"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def idGetIt():
    return "من که نفهمیدم، بالاخره چی شد؟ پیامام چجوری باشه؟"


def getCanceledMidway(userId):
    message = "laelahaelalah, berim az aval pas\ndobare shomare daneshjuEt ro vared kon."
    if getStyle(userId)==FA:
        message = "laelahaelalah، بریم از اول پس. وارد کن دوباره شماره دانشجوییت رو"
        return message
    elif getStyle(userId)==LAELAHAELALAH:
        return message

def getNotAuth(userId):
    return "moteasefane shomare daneshjuE shoma tuye database vujud nadarad lotfan be @NeginKheirmand ya @CEshora_admin khabar bede "
    