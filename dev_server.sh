#!/bin/sh

uwsgi --plugin python \
    --http-socket :8090 \
    --wsgi-file saveserver.py