#!/bin/bash
sleep 5
python certificates_test/manage.py migrate
python certificates_test/manage.py runserver 0:8000
