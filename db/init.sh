#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_DATABASE" <<-EOSQL
    ALTER USER "$DB_USER" WITH PASSWORD '$DB_PASSWORD';
    CREATE ROLE $DB_REPL_USER REPLICATION LOGIN PASSWORD '$DB_REPL_PASSWORD';
    CREATE TABLE emails( id serial PRIMARY KEY,email VARCHAR (100) NOT NULL);
    CREATE TABLE phone_numbers( id serial PRIMARY KEY,phone_number VARCHAR (20) NOT NULL);
EOSQL


echo "Editing conf"
sed -i "s/#archive_mode = off/archive_mode = on/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/#archive_command = ''/archive_command = 'mkdir -p \/var\/lib\/postgresql\/data\/pg_archive\/ && cp %p \/var\/lib\/postgresql\/data\/pg_archive\/%f'/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/#max_wal_senders = 10/max_wal_senders = 10/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/#wal_level = replica/wal_level = replica/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/#wal_log_hints = off/wal_log_hints = on/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/#log_replication_commands = off/log_replication_commands = on/" /var/lib/postgresql/data/postgresql.conf

# Update pg_hba.conf
echo "Editing pg_hba"
echo "host replication all 11.0.0.0/24 md5" >> /var/lib/postgresql/data/pg_hba.conf

exec "$@"