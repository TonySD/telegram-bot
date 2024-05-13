import psycopg2
import os, logging
import config
from typing import Dict

class DB:
    # Needed for temporary saving before saving in DB
    chat_buffer: Dict[int, str]

    def __init__(self):
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_DATABASE")
        self.chat_buffer = dict()

    def open_connection(self):
        logging.debug("Connection to DB had been opened")
        return psycopg2.connect(user=self.username,
                                password=self.password,
                                host=self.host,
                                port=self.port, 
                                database=self.database)

    # Use only internally
    def execute_command_commit(self, command: str):
        connection = None
        try:
            connection = self.open_connection()
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
            logging.info(f"Command {command} was succesfully executed")
        except(Exception, psycopg2.Error) as error:
            logging.error(f"Ошибка при работе с PostgreSQL: {error}, command: {command}")
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.debug("Connection with PostgreSQL is closed")

    # Use only internally
    def execute_command_fetch(self, command: str):
        connection = None
        result = list()
        try:
            connection = self.open_connection()
            cursor = connection.cursor()
            cursor.execute(command)
            data = cursor.fetchall()
            result.extend(data)
            logging.info(f"Command [{command}] was succesfully executed")
        except(Exception, psycopg2.Error) as error:
            logging.error(f"Error PostgreSQL: {error}, command: {command}")
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.debug("Connection with PostgreSQL is closed")
        return result

    def select_emails(self):
        return self.execute_command_fetch("SELECT * FROM emails;")

    def select_phones(self):
        return self.execute_command_fetch("SELECT * FROM phone_numbers;")

    def insert_phones(self, phone_numbers):
        phones = ", ".join([f"('{phone}')" for phone in phone_numbers])
        statement = "INSERT INTO phone_numbers (phone) VALUES %s;" % phones
        self.execute_command_commit(statement)

    def insert_emails(self, emails):
        emails = ", ".join([f"('{email}')" for email in emails])
        statement = "INSERT INTO emails (email) VALUES %s;" % emails
        self.execute_command_commit(statement)

    def store_in_buffer(self, chat_id: int, values: list):
        self.chat_buffer[chat_id] = values
        logging.debug(f"Added values {values} in buffer")

    # Mode 0 - phones, 1 - emails
    def save_in_db(self, chat_id: int, mode: int):
        if chat_id not in self.chat_buffer:
            logging.error(f"Chat_id {chat_id} not in buffer, but tried to send values")
            return
        
        values = self.chat_buffer.pop(chat_id)
        logging.debug(f"Extracted values {values} from buffer")
        if mode == 0:
            self.insert_phones(values)
            logging.info(f"Phones {values} sended to DB")
        if mode == 1:
            self.insert_emails(values)
            logging.info(f"Emails {values} sended to DB")
        

    def delete_from_buffer(self, chat_id):
        if chat_id not in self.chat_buffer:
            logging.error(f"Chat_id {chat_id} not in buffer, but tried to clear")
            return
        
        values = self.chat_buffer.pop(chat_id)
        logging.debug(f"Extracted values {values} from buffer")

my_db = DB()