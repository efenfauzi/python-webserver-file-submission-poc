FROM python:2.7-onbuild

EXPOSE 8090
CMD [ "python", "./gunicorn_flask.py" ]
