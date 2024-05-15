#!/bin/bash

pg_ctl stop -D /var/lib/postgresql/data
rm -rf /var/lib/postgresql/data/*

until pg_basebackup -R -h db -U repl_user -D /var/lib/postgresql/data -P; do
    echo 'Master server is not launched yet...'
    sleep 5s
done

echo 'Master server connection done!'
service postgresql start