#!/usr/bin/env python

from __future__ import print_function

import os
import tempfile
import time

import flask
import psutil
import werkzeug

from saveserver import current_milli_time, intWithCommas, measure_spent_time

app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''}, methods = ['POST'])
@app.route('/<path:path>', methods = ['POST'])
def hello(path):
    app.logger.info('new request')
    def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
        tmpfile = tempfile.NamedTemporaryFile('wb+', prefix='flaskapp')
        app.logger.info("start receiving file ... filename => " + str(tmpfile.name))
        return tmpfile
    ms = measure_spent_time()
    
    stream,form,files = werkzeug.formparser.parse_form_data(flask.request.environ, stream_factory=custom_stream_factory)
    total_size = 0
    
    for fil in files.values():
        app.logger.info(" ".join(["saved form name", fil.name, "submitted as", fil.filename, "to temporary file", fil.stream.name]))
        total_size += os.path.getsize(fil.stream.name)
    mb_per_s = "%.1f" % ((total_size / (1024.0*1024.0)) / ((1.0+ms(raw=True))/1000.0))
    app.logger.info(" ".join([str(x) for x in ["handling POST request, spent", ms(), "ms.", mb_per_s, "MB/s.", "Number of files:", len(files.values())]]))
    process = psutil.Process(os.getpid())
    app.logger.info("memory usage: %.1f MiB" % (process.memory_info().rss / (1024.0*1024.0)))

    return "Hello World!"

if __name__ == "__main__":
    app.run(port=8090)
