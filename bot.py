import logging, os, re
from typing import List
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
TOKEN = os.getenv("TOKEN")
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))      # I work from parent dir, but want to collect logs in file's dir
if not (Path(WORKING_DIRECTORY) / "logs").is_dir():                 # If logs dir not exists, create it
    os.makedirs(Path(WORKING_DIRECTORY) / "logs")
NUMBER_OF_LOGS = len(os.listdir(Path(WORKING_DIRECTORY) / "logs/")) # To have various log files for launches



logging.basicConfig(level=logging.DEBUG, 
                    filename=Path(WORKING_DIRECTORY) / f"logs/log{NUMBER_OF_LOGS}.txt", 
                    format=' %(asctime)s - %(levelname)s - %(message)s'
)

def findPhoneNumbersCommand(update: Update, context) -> str:
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_numbers'

def findEmailsCommand(update: Update, context) -> str:
    update.message.reply_text('Введите текст для поиска адресов электронных почт: ')
    logging.info(f"{update.message.chat_id} triggered find emails command")

    return 'find_emails'

def find_emails_in_strings(strings: str | List[str]) -> List[str]:
    result = list()
    emailRegex = re.compile(r"[\w\-+.]+@[\w\-+.]+\.[A-Za-z]+")
    if type(strings) == str:
        strings = [strings]

    for string in strings:
        result.extend(
            emailRegex.findall(string)
        )

    logging.debug(f"Func: Email find: {strings}, \n\t\treturned: {result}")
    return result


def find_phone_numbers(strings: str | List[str]) -> List[str]:
    result = list()
    phoneRegex = re.compile(r"(\+7|8)[ \-]?\(?(\d{3})\)?[ \-]?(\d{3})[ \-]?(\d{2})[ \-]?(\d{2})")
    if type(strings) == str:
        strings = [strings]

    for string in strings:
        result.extend(
            map(''.join,
                phoneRegex.findall(string)
            )
        )

    logging.debug(f"Func: Phone find\nGot: {strings}, \nreturned: {result}")
    return result

def findEmailsCommandIntermediary(update: Update, context) -> str:
    text = update.message.text
    logging.debug(f"Got {update.message.chat_id} text for email find")
    found_emails = find_emails_in_strings(text)
    logging.info(f"Email job done. Found {len(found_emails)} emails")

    if not found_emails: 
        update.message.reply_text('Электронные почты не найдены')
        return
    
    response = list()
    response.append(f"Найдены {len(found_emails)} адресов:")
    for i, email in enumerate(found_emails):
        response.append(f"{i}: {email}")
    logging.debug(f"Created response for emails: {response}")
    update.message.reply_text("\n".join(response))
    
def findPhoneNumbersCommandIntermediary(update: Update, context) -> str:
    text = update.message.text
    logging.debug(f"Got {update.message.chat_id} text for phones")
    found_phones = find_phone_numbers(text)
    logging.info(f"Phone job done. Found {len(found_phones)} phones")

    if not found_phones: 
        update.message.reply_text('Телефонные номера не найдены')
        return
    
    response = list()
    response.append(f"Найдены {len(found_phones)} номеров:")
    for i, phone in enumerate(found_phones):
        response.append(f"{i}: {phone}")
    logging.debug(f"Created response for phones: {response}")
    update.message.reply_text("\n".join(response))
    

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    


if __name__ == "__main__":
    main()
