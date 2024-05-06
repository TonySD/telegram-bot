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
COMMAND_DESCRIPTIONS = (
    ("find_phone_number", "Команда для поиска телефонных номеров"),
    ("find_email", "Команда для поиска электронных почт"),
    ("verify_password", "Команда для определения сложности пароля")
)


logging.basicConfig(level=logging.DEBUG, 
                    filename=Path(WORKING_DIRECTORY) / f"logs/log{NUMBER_OF_LOGS}.txt", 
                    format=' %(asctime)s - %(levelname)s - %(message)s'
)

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!\nВведи /help, чтобы узнать, что я умею!')

def helpCommand(update: Update, context):
    response = list()
    response.append("Вот список комманд, которые я могу выполнить:")
    for command_name, description in COMMAND_DESCRIPTIONS:
        response.append(f"/{command_name}: {description}")
    update.message.reply_text("\n".join(response))

# Email section

def findEmails(strings: str | List[str]) -> List[str]:
    result = list()
    emailRegex = re.compile(r"[\w\-+.]+@[\w\-+.]+\.[A-Za-z]+")
    if type(strings) == str:
        strings = [strings]

    for string in strings:
        result.extend(
            emailRegex.findall(string)
        )

    logging.debug(f"Func: Email find\nGot: {strings}, \n\t\treturned: {result}")
    return result

def findEmailsCommand(update: Update, context) -> str:
    update.message.reply_text('Введите текст для поиска адресов электронных почт: ')
    logging.info(f"{update.effective_user.full_name} triggered find emails command")

    return 'find_email'

def findEmailsCommandIntermediary(update: Update, context):
    text = update.message.text
    logging.debug(f"Got {update.message.chat_id} text for email find")
    found_emails = findEmails(text)
    logging.info(f"Email job done. Found {len(found_emails)} emails")

    if not found_emails: 
        update.message.reply_text('Электронные почты не найдены')
        return ConversationHandler.END
    
    response = list()
    response.append(f"Найдены {len(found_emails)} адресов:")
    for i, email in enumerate(found_emails):
        response.append(f"{i}: {email}")
    logging.debug(f"Created response for emails: {response}")
    update.message.reply_text("\n".join(response))
    return ConversationHandler.END

# Phone section

def findPhoneNumbers(strings: str | List[str]) -> List[str]:
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

def findPhoneNumbersCommand(update: Update, context) -> str:
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    logging.info(f"{update.effective_user.full_name} triggered find phones command")

    return 'find_phone_number'
    
def findPhoneNumbersCommandIntermediary(update: Update, context):
    text = update.message.text
    logging.debug(f"Got {update.message.chat_id} text for phones")
    found_phones = findPhoneNumbers(text)
    logging.info(f"Phone job done. Found {len(found_phones)} phones")

    if not found_phones: 
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END
    
    response = list()
    response.append(f"Найдены {len(found_phones)} номеров:")
    for i, phone in enumerate(found_phones):
        response.append(f"{i}: {phone}")
    logging.debug(f"Created response for phones: {response}")
    update.message.reply_text("\n".join(response))
    return ConversationHandler.END

# Password section

def verifyPassword(string: str) -> bool | None:
    passwordRegex = re.compile("[^\s]+")
    password = passwordRegex.search(string).group()
    if not password:
        logging.debug(f"Received blank string: [{string}]")
        return None
    lengthRegex = re.compile("[^\s]{8,}")
    uppercaseRegex = re.compile("[A-Z]")
    lowercaseRegex = re.compile("[a-z]")
    digitsRegex = re.compile("\d")
    specialSymbolsRegex = re.compile("[!@#$%^&*()]")

    if lengthRegex.search(password) and uppercaseRegex.search(password) and lowercaseRegex.search(password) and digitsRegex.search(password) and specialSymbolsRegex.search(password):
        logging.debug(f"Password {password} is strong")
        return True
    
    logging.debug(f"Password {password} is weak")
    return False

def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите ваш пароль для проверки: ')
    logging.info(f"{update.effective_user.full_name} triggered verify password command")

    return 'verify_password'

def verifyPasswordCommandIntermediary(update: Update, context):
    text = update.message.text
    logging.debug(f"Got {update.message.chat_id} text for verifying password")
    password_difficulty = verifyPassword(text)

    if password_difficulty is None: 
        update.message.reply_text('Введите корректный пароль')
        return

    logging.info(f"Password job done. Password is {'strong' if password_difficulty else 'weak'}")
    response = str()
    if password_difficulty:
        response = "Пароль сложный"
    else:
        response = "Пароль простой"

    update.message.reply_text(response)
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbersCommandIntermediary)],
        },
        fallbacks=[]
    )

    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, findEmailsCommandIntermediary)],
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verifyPasswordCommandIntermediary)],
        },
        fallbacks=[]
    )

    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPassword)
		
    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
