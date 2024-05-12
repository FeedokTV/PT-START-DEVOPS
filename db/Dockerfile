FROM postgres:14

EXPOSE $DB_PORT

WORKDIR /app
RUN chmod 755 -R /app
RUN mkdir -p /var/log/postgres

RUN chmod -R 777 /var/log/postgres