#!/bin/bash

# Verifica se o n  mero correto de argumentos foi passado
if [ "$#" -ne 5 ]; then
    echo "Uso: $0 <host> <hostname> <username> <password> <base_backup_dir>"
    exit 1
fi

# Atribui os argumentos a vari  veis
HOST="$1"
HOSTNAME="$2"
USERNAME="$3"
PASSWORD="$4"
BASE_BACKUP_DIR="$5"

# Chama o script Python com as vari  veis
python3 /usr/lib/zabbix/externalscripts/backup_mk.py "$HOST" "$HOSTNAME" "$USERNAME" "$PASSWORD" "$BASE_BACKUP_DIR"
