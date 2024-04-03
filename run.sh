#!/bin/bash

until nc -z "${DATABASE_HOST}" "${DATABASE_PORT}"; do
    echo "$(date) - waiting for postgres..."
    sleep 1
done

until nc -z "${MQTT_HOST}" "${MQTT_PORT}"; do
    echo "$(date) - waiting for mosquitto..."
    sleep 1
done

python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py createsuperuser --noinput
python manage.py runserver "${GATEWAY_HOST}":"${GATEWAY_PORT}"