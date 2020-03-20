#!/bin/bash

if [ "$FLASK_ENV" = "development" ] ; then python3 ./import.py ; fi

exec "$@"