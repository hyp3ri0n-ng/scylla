#!/bin/bash

scyllaenv/bin/gunicorn -w 10 -b 0.0.0.0:80 scylla:app
#scyllaenv/bin/gunicorn -w 10 --timeout 999999 -b 0.0.0.0:80 scylla:app
