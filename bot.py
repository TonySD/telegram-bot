import logging, os, re, paramiko
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
    ("verify_password", "Команда для определения сложности пароля"),
    ("get_release", "Получить информацию о релизе"),
    ("get_uname", "Получить информацию об архитектуре процессора, имени хоста системы и версии ядра"),
    ("get_uptime", "Получить время работы"),
    ("get_df", "Получение информации о состоянии файловой системы"),
    ("get_free", "Получение информации о состоянии оперативной памяти"),
    ("get_mpstat", "Получение информации о производительности системы"),
    ("get_w", "Получение информации о работающих в данной системе пользователях"),
    ("get_auths", "Получение информации о последних 10 входов в систему"),
    ("get_critical", "Получение информации о последних 5 критических событиях"),
    ("get_ps", "Получение информации о запущенных процессах"),
    ("get_ss", "Получение информации об используемых портах"),
    ("get_apt_list", "Получение информации об установленных пакетах. Присутствуют 2 режима: вывод всех пакетов и поиск информации о конкретном"),
    ("get_services", "Получение информации о запущенных сервисах"),
    ("get_repl_logs", "Получение логов о репликации")
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

# Monitoring

def executeCommand(command: str) -> str | None:
    if not command:
        logging.error(f"Func executeCommand got blank command: {command}")
        return

    host = os.getenv('HOST')
    port = os.getenv('PORT')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(command)
    data = stdout.read() + stderr.read()
    stdin.close()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]

    logging.debug(f"Executed {command}. Result: {data}")
    return data

def sendPackets(data: str, update: Update):
    data = data.split('\n')
    for i in range(0, len(data), 20):
        update.message.reply_text("\n".join(data[i : i + 20]))

def getRelease(update: Update, context):
    data = executeCommand("cat /etc/*-release")
    update.message.reply_text(f"Вот информация: \n{data}")

def getUname(update: Update, context):
    data = executeCommand("uname -a")
    update.message.reply_text(f"Вот информация: \n{data}")

def getUptime(update: Update, context):
    data = executeCommand("uptime")
    update.message.reply_text(f"Вот информация: \n{data}")

def getDF(update: Update, context):
    data = executeCommand("df -h")
    update.message.reply_text(f"Вот информация: \n{data}")

def getFree(update: Update, context):
    data = executeCommand("free -h")
    update.message.reply_text(f"Вот информация: \n{data}")

def getMpstat(update: Update, context):
    data = executeCommand("mpstat")
    update.message.reply_text(f"Вот информация: \n{data}")

def getW(update: Update, context):
    data = executeCommand("uptime")
    update.message.reply_text(f"Вот информация: \n{data}")

def getAuths(update: Update, context):
    data = executeCommand("last | head")
    update.message.reply_text(f"Вот информация: \n{data}")

def getCritical(update: Update, context):
    data = executeCommand("journalctl -r -p crit -n 5")
    update.message.reply_text(f"Вот информация: \n{data}")

def getPs(update: Update, context):
    data = executeCommand("ps")
    update.message.reply_text(f"Вот информация: \n{data}")

def getSs(update: Update, context):
    data = executeCommand("ss")
    update.message.reply_text(f"Вот информация: \n")
    sendPackets(data, update)

def getAllAptList(update: Update) -> str:
    data = executeCommand("apt list | head -n 200")
    sendPackets(data, update)

def getSpecificAptInfo(update: Update, context):
    text = update.message.text
    packetRegex = re.compile(r"[A-Za-z0-9.-]+")
    packet = packetRegex.search(text).group()
    if not packet:
        update.message.reply_text(f"Введите корректное имя пакета")
        return    
    logging.info(f"Requested info about {packet.strip()}")
    data = executeCommand(f"apt info {packet.strip()}")
    update.message.reply_text(f"Информация о пакете {packet}:")
    sendPackets(data, update)
    return ConversationHandler.END

def getAptListCommand(update: Update, context):
    update.message.reply_text(f"Данная комманда поддерживает два режима.\n1. Вывод всех пакетов.\n2. Поиск информации о введенном пакете.\nВведите номер режима, который вас интересует")
    return 'enter_mode_number'

def enterAptMode(update: Update, context):
    if update.message.text.strip() not in ('1', '2'):
        logging.info(f"{update.effective_user.full_name} entered not valid mode: {update.message.text}")
        update.message.reply_text(f"Пожалуйста, выберите режим, отправив 1 или 2")

    logging.debug(f"Chosed {update.message.text.strip()} mode")
    if update.message.text.strip() == '1':
        update.message.reply_text(f"Вы выбрали режим вывода всех пакетов")
        getAllAptList(update)
        return ConversationHandler.END

    update.message.reply_text(f"Вы выбрали режим вывода информации о конкретном пакете")
    update.message.reply_text(f"Введите имя пакета, о котором вы хотите узнать")
    return "get_specific_apt_info"

def getServices(update: Update, context):
    data = executeCommand("systemctl list-units --type=service | cat")
    update.message.reply_text(f"Вот информация: \n")
    sendPackets(data, update)

def getReplLogs(update: Update, context):
    data = executeCommand("cat /var/log/postgresql/postgresql-15-main.log | grep -i 'repl_user' | head -n 20") 
    update.message.reply_text(f"Вот информация: {data}\n")

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

    convHandlerAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptListCommand)],
        states={
            'enter_mode_number': [MessageHandler(Filters.text & ~Filters.command, enterAptMode)],
            'get_specific_apt_info': [MessageHandler(Filters.text & ~Filters.command, getSpecificAptInfo)],
        },
        fallbacks=[]
    )

    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(convHandlerAptList)

    dp.add_handler(CommandHandler("get_release", getRelease))
    dp.add_handler(CommandHandler("get_uname", getUname))
    dp.add_handler(CommandHandler("get_uptime", getUptime))
    dp.add_handler(CommandHandler("get_df", getDF))
    dp.add_handler(CommandHandler("get_free", getFree))
    dp.add_handler(CommandHandler("get_mpstat", getMpstat))
    dp.add_handler(CommandHandler("get_w", getW))
    dp.add_handler(CommandHandler("get_auths", getAuths))
    dp.add_handler(CommandHandler("get_critical", getCritical))
    dp.add_handler(CommandHandler("get_ps", getPs))
    dp.add_handler(CommandHandler("get_ss", getSs))
    dp.add_handler(CommandHandler("get_services", getServices))
    dp.add_handler(CommandHandler("get_repl_logs", getReplLogs))
		
    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
