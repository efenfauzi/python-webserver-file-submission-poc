from __future__ import print_function

import os
import tempfile
import time

import werkzeug


def current_milli_time():
    return int(round(time.time() * 1000))

def intWithCommas(x):
    # There is no 'long integer' in Python 3 anymore.
    # https://docs.python.org/3.7/library/stdtypes.html#numeric-types-int-float-complex
    # if type(x) not in [type(0), type(0L)]:
    #     raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)

def measure_spent_time():
    start = current_milli_time()
    diff = { 'res' : None }
    def get_spent_time(raw=False):
        if diff['res'] == None:
            diff['res'] = current_milli_time() - start
        if raw:
            return diff['res']
        else:
            return intWithCommas(diff['res']) 
    return get_spent_time

def application(environ, start_response):
    response_body = b'Works fine'
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
    ]

    if environ.get('REQUEST_METHOD', 'GET') == 'POST':
        ms = measure_spent_time()
        print("*"*80)

        def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
            tmpfile = tempfile.NamedTemporaryFile('wb+')
            return tmpfile

        stream,form,files = werkzeug.formparser.parse_form_data(environ, stream_factory=custom_stream_factory)
        total_size = 0
        for fil in files.values():
            print("saved form name", fil.name, "submitted as", fil.filename, "to temporary file", fil.stream.name)
            total_size += os.path.getsize(fil.stream.name)
        mb_per_s = "%.1f" % ((total_size / (1024.0*1024.0)) / ((1.0+ms(raw=True))/1000.0))
        print("handling POST request, spent", ms(), "ms.", mb_per_s, "MB/s")

    start_response(status, response_headers)
    return [response_body]
