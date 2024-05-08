import os, logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))      # I work from parent dir, but want to collect logs in file's dir
if not (Path(WORKING_DIRECTORY) / "logs").is_dir():                 # If logs dir not exists, create it
    os.makedirs(Path(WORKING_DIRECTORY) / "logs")
NUMBER_OF_LOGS = len(os.listdir(Path(WORKING_DIRECTORY) / "logs/")) # To have various log files for launches
COMMAND_DESCRIPTIONS = (
    ("find_phone_number", "Команда для поиска телефонных номеров"),
    ("find_email", "Команда для поиска электронных почт"),
    ("get_phone_numbers", "Команда для вывода имеющихся в БД телефонных номеров"),
    ("get_emails", "Команда для вывода имеющихся в БД электронных почт"),
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