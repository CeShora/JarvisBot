
import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from messages import * 


API_KEY = os.getenv('API_KEY')

# for logging in the host server, just in case ;) 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """when student uses command /start """
    global start_message
    update.message.reply_text(start_message)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    global API_KEY
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # for loging all errors when ocurred 
    dp.add_error_handler(error)

    # to start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()