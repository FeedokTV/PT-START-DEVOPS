#!/bin/bash
set -e

pg_ctl stop

rm -r /var/lib/postgresql/data/*

echo "Waiting for master to ping..."
sleep 10s
pg_basebackup -h db -U $DB_REPL_USER -D /var/lib/postgresql/data --wal-method=stream --write-recovery-conf

pg_ctl start

exec "$@"