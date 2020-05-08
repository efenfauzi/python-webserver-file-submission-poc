#!/bin/sh

set -ex

docker build --tag=docker.nsd.no/programvareutvikling/python-file-submission-poc .

docker run -it --memory="100M" --publish=8090:8090 docker.nsd.no/programvareutvikling/python-file-submission-poc
