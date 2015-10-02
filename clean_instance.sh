#!/bin/bash

# Clean instance to avoid conflicts.
# We require a stateless server, so there should not
# be any instance exclusive files

rm -rf /srv/app/*