#! /bin/sh

sleep 1m # sleep 1 minute so to ensure internet connection
MSG=$(ifconfig)
python3 send_email.py -a <address> -p <password> -m "$MSG"
