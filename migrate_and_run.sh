#! /bin/bash

chmod +x ./manage.py
./manage.py migrate
./manage.py runserver 0:8080
