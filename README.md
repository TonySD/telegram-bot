# Docker branch

## To build project:
1. Create .env file with such info:
```
TOKEN = token - будет содержать токен бота
RM_HOST = rm_host - будет содержать удаленный хост, который будем мониторить
RM_PORT = rm_port - будет содержать порт удаленного хоста, к которому будем подключаться
RM_USER = rm_user - будет содержать пользователя удаленного хоста
RM_PASSWORD = rm_password - будет содержать пароль пользователя удаленного хоста
DB_USER = db_user - будет содержать пользователя базы данных удаленного хоста
DB_PASSWORD = db_password - будет содержать пароль пользователя базы данных удаленного хоста
DB_HOST = db_host - будет содержать хост(имя контейнера), в котором будет работать база данных
DB_PORT = db_port - будет содержать порт, на котором работает база данных
DB_DATABASE = db_database - будет содержать имя базы данных
DB_REPL_USER = db_repl_user - будет содержать пользователя реплицируемой базы данных
DB_REPL_PASSWORD = db_repl_password - будет содержать пароль пользователя реплицируемой базы данных
DB_REPL_HOST = db_repl_host - будет содержать хост(имя контейнера), в котором будет работать реплицируемая база данных
DB_REPL_PORT = db_repl_port - будет содержать порт, на котором работает реплицируемая база данных
```
2. docker compose build
3. docker compose up -d
4. Enjoy!
