#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import multiprocessing
import os
import re
import sys
import uuid
from logging import StreamHandler

import gunicorn.app.base
from gunicorn.six import iteritems

import flask_app


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    # See https://github.com/benoitc/gunicorn/blob/6a3bd70d2b6a8961f8bb1c16df58b4d7a3e83836/gunicorn/config.py
    # for values
    options = {
        'workers' : (multiprocessing.cpu_count() * 2) + 1,
        'logconfig' : 'gunicorn_logging.conf',
        'timeout': 60*25, # 25 minutes timeout for worker process 
        'bind' : '0.0.0.0:8090'
    }
    StandaloneApplication(flask_app.app, options).run()
