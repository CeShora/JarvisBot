import redis
import datetime
r = redis.Redis(host='localhost', port=6379, db=0)

def admin(update, context):
    update.message.reply_text("Hi admin👋")
    name = "data-"+str(datetime.datetime.now())+".txt"
    f = open( name , "w")
    
    # write the data collected into a file and send it to the admin 
    for key in r.keys():
        a = str(key)+"  "+str( r.get(key))
        f.write(a)
    f.flush()
    f.close()
    update.message.reply_document(name, caption= "the data collected until now\n"+str(datetime.datetime.now()))
    return None

def getData(update, context):
    update.message.reply_text("Hi admin👋")
    target = update.message.text
    data = []
    for key in r.keys():
        if target in str(key) or target in str(r.get(key)):
            data.append(str(r.get(key)))
    x = " ".join(data)
    if not x == "" :
        update.message.reply_text(x)
    else:
        update.message.reply_text("Couldn't find the target😓")
    return None

def imDumb(update, context):
    update.message.reply_text("sorry admin, im dumb😞, i cant understand you :(")
    return None





##########################################################################
# this one will just notify admin when there is a change in the database #
##########################################################################
def notifyAdmin(admin_id, redisInstance, context):
    a = ""
    for key in r.keys():
        a = str(key)+"  "+str( r.get(key))+"\n"
    context.bot.send_message(chat_id=admin_id, text=a) 
    return 
