==========
Deployment
==========

This project relies on Environment variables.

Please make sure you define the variables according to the `Settings <settings.html>`_ page:


Deployment to Production on AWS
-------------------------------

System requirements for Debian based servers: requirements.apt

Python requirements: requirements.txt


It was succesfully tested and mounted on AWS using Python Virtualenv, UWSGI and NGINX.

UWSGI Configuration
-------------------

::

    [uwsgi]
    vhost = true
    plugins = python
    socket = /tmp/ekratia.sock
    master = true
    enable-threads = true
    processes = 4
    wsgi-file = /srv/apps/ekratia/config/wsgi.py
    virtualenv = /home/ubuntu/.virtualenvs/env
    chdir = /srv/apps/ekratia/


Nginx Configuration
-------------------
::

    server {
        listen 80;
        access_log /var/log/nginx/ekratia.access.log;
        error_log /var/log/nginx/ekratia.error.log;

        location / {
            uwsgi_pass      unix:///tmp/ekratia.sock;
            include     uwsgi_params;
        }
    }


The used services were:
::

    Amazon EC2
    Amazon RDS PostgresSQL
    Amazon S3
