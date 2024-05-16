#!/bin/bash

declare -A env_vars
while IFS='=' read -r key value || [ -n "$key" ]; do
    if [[ "$key" && "$value" ]]; then
        env_vars["$key"]="$value"
    fi
done < .env

env_vars["DB_REPL_HOST"]="192.168.0.66"

for key in "${!env_vars[@]}"; do
    echo "$key: ${env_vars[$key]}"
done > env.yaml

ansible-playbook playbook_tg_bot.yml --extra-vars "@env.yaml"