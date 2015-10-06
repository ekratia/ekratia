#!/bin/bash

# Reload app server
# If any other operation is required, this is the place
# (start daemons, etc)

service uwsgi stop
service uwsgi start