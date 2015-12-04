Deployment
===========

Deploy to AWS
-------------

::

    grunt deploy

Environment variables required from the AWS S3 Bucket:

::

    AWS_ACCESS_KEY_ID, 
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME


Deployment to Production on AWS
-------------------------------

The API application can be deployed using Docker. The specifications are
in the file docker-compose.yml

System requirements for Debian based servers: requirements.apt

Python requirements: requirements.txt

In order to run this application in production. The following
environment variables need to be defined:

DJANGO_SETTINGS_MODULE DJANGO_SECRET_KEY DJANGO_ALLOWED_HOSTS
DJANGO_AWS_ACCESS_KEY_ID DJANGO_AWS_SECRET_ACCESS_KEY
DJANGO_AWS_STORAGE_BUCKET_NAME DJANGO_DATABASE_URL

It was succesfully tested and mounted on AWS using Python Virtualenv,
UWSGI and NGINX.

The used services were: Amazon EC2 Amazon RDS PostgresSQL Amazon S3