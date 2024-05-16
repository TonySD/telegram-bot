sudo service ssh restart
service postgresql start

initdb
pg_ctl start
echo "host replication $DB_REPL_USER 172.30.0.0/24 trust" >> /var/lib/postgresql/data/pg_hba.conf 
echo "host all all 172.30.0.0/24 trust" >> /var/lib/postgresql/data/pg_hba.conf 
psql -U postgres -c "CREATE database $DB_DATABASE;" 
psql -U postgres -d bot_db -f /docker-entrypoint-initdb.d/01_create_repl_user.sql
psql -U postgres -d bot_db -f /docker-entrypoint-initdb.d/02_create_tables.sql
psql -U postgres -d bot_db -f /docker-entrypoint-initdb.d/03_insert_test_data.sql
pg_ctl stop 

postgres -c 'listen_addresses=*' -c 'archive_mode=on' -c 'archive_command=cp %p /oracle/pg_data/archive/%f' -c 'max_wal_senders=10' -c 'wal_level=replica' -c 'wal_log_hints=on' -c 'log_directory=/var/log/postgresql/' -c 'log_filename=postgres.log' -c 'logging_collector=on' -c 'log_replication_commands=on'

