#!/bin/bash

#Creates a virtualenv if it does not exist and uses it
if [ ! -d ~/.envs/django-app ] ; then
    virtualenv ~/.envs/django-app
fi

source ~/.envs/django-app/bin/activate

pip --version >/dev/null 2>&1 || {
    echo >&2 -e "\npip is required but it's not installed."
    echo >&2 -e "You can install it by running the following command:\n"
    echo >&2 "wget https://bootstrap.pypa.io/get-pip.py; chmod +x get-pip.py; sudo ./get-pip.py"
    echo >&2 -e "\n"
    echo >&2 -e "\nFor more information, see pip documentation: https://pip.pypa.io/en/latest/"
    exit 1;
}

virtualenv --version >/dev/null 2>&1 || {
    echo >&2 -e "\nvirtualenv is required but it's not installed."
    echo >&2 -e "You can install it by running the following command:\n"
    echo >&2 "sudo pip install virtualenv"
    echo >&2 -e "\n"
    echo >&2 -e "\nFor more information, see virtualenv documentation: https://virtualenv.pypa.io/en/latest/"
    exit 1;
}

if [ -z "$VIRTUAL_ENV" ]; then
    echo >&2 -e "\nYou need activate a virtualenv first"
    echo >&2 -e 'If you do not have a virtualenv created, run the following command to create and automatically activate a new virtualenv named "venv" on current folder:\n'
    echo >&2 -e "virtualenv venv"
    echo >&2 -e "\nTo leave/disable the currently active virtualenv, run the following command:\n"
    echo >&2  "deactivate"
    echo >&2 -e "\nTo activate the virtualenv again, run the following command:\n"
    echo >&2  "source venv/bin/activate"
    echo >&2 -e "\nFor more information, see virtualenv documentation: https://virtualenv.pypa.io/en/latest/"
    echo >&2 -e "\n"
    exit 1;
else
    echo >&2 -e "$VIRTUAL_ENV"
    pip install -r /srv/app/requirements.txt
    cp /home/ubuntu/.env /srv/app/
    python /srv/app/manage.py migrate --settings=config.settings.production
    python /srv/app/manage.py collectstatic --settings=config.settings.production --noinput > /dev/null 2> /dev/null < /dev/null &
fi
