import psycopg2
import os, logging
import config

class DB:
    def __init__(self):
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_DATABASE")

    def open_connection(self):
        logging.debug("Connection to DB had been opened")
        return psycopg2.connect(user=self.username,
                                password=self.password,
                                host=self.host,
                                port=self.port, 
                                database=self.database)

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

    def select_emails():
        ...

    def select_phones():
        ...

    def insert_phones():
        ...

    def insert_emails():
        ...

my_db = DB()