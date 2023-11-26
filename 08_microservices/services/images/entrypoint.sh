#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# prvotni vytvoreni a naplneni tabulek
if [ "$DB_INIT" = "1" ]
then
    echo "Creating the database tables..."
    python manage.py create_db
    echo "Tables created"

    echo "Filling the database tables..."
    python manage.py seed_db
    echo "Tables filled"

fi

exec "$@"