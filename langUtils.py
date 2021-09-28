
import redis
import json

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
    grandChildText = "bah bah, umadi nave tahvil begiri?"
    if getStyle(userId)==FA:
        grandChildText = "به به اومدی بچه تحویل بگیری؟"
        return grandChildText
    elif getStyle(userId)==LAELAHAELALAH:
        return grandChildText