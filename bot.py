import logging, os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from dotenv import load_dotenv
from pathlib import Path

TOKEN = os.getenv("TOKEN")
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))      # I work from parent dir, but want to collect logs in file's dir
if not (Path(WORKING_DIRECTORY) / "logs").is_dir():                 # If logs dir not exists, create it
    os.makedirs(Path(WORKING_DIRECTORY) / "logs")
NUMBER_OF_LOGS = len(os.listdir(Path(WORKING_DIRECTORY) / "logs/")) # To have various log files for launches

load_dotenv()

logging.basicConfig(level=logging.DEBUG, 
                    filename=Path(WORKING_DIRECTORY) / f"logs/log{NUMBER_OF_LOGS}.txt", 
                    format=' %(asctime)s - %(levelname)s - %(message)s'
)

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_numbers'

def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска адресов электронных почт: ')

    return 'find_emails'

def find_emails():
    ...

def find_phone_numbers():
    ...

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher


if __name__ == "__main__":
    main()
