# python-webserver-file-submission-poc

## How to handle large multipart/form-data POST request file uploads in Python using werkzeug and uwsgi

### Fork project from https://gitlab.nsd.uib.no/ire/python-webserver-file-submission-poc 

	bump to python 3.7

### Start server locally

    $ pip install -r ./requirements.txt

    $ ./dev_server.sh

### Or: Start server using docker

    $ ./docker_server.sh

POST a big file to the server:

    curl -XPOST -F "file=@./my.big.file.bin" "http://localhost:8090/"

Watch the console output or see the file [saveserver.py](saveserver.py).

The file(s) will not reside in memory, but be streamed directly to disk.
Posting e.g. a 10 GiB file should not be a problem.
