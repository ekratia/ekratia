============
Installation
============

Clone the ``Ekratia`` repository::

    $ git clone git@github.com:ekratia/ekratia.git

This project was created using cookiecutterdjango_

.. cookiecutterdjango_: https://github.com/pydanny/cookiecutter-django

Setup project locally
---------------------

.. index:: pip, virtualenv, PostgreSQL

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the os dependencies::

    $ sudo ./install_os_dependencies.sh install

Then install the requirements for your local development::

    $ pip install -r requirements/local.txt

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then, create a PostgreSQL database with the following command. We will call the 
database ``ekratia``

    $ createdb ekratia

You can now run the usual Django ``migrate`` and ``runserver`` command::

    $ python manage.py migrate

    $ python manage.py runserver


**Live reloading and Sass CSS compilation**

If you'd like to take advantage of live reloading and Sass / Compass CSS compilation you can do so with the included Grunt task.

Make sure that nodejs_ is installed. Then in the project root run::

    $ npm install

.. _nodejs: http://nodejs.org/download/

Now you just need::

    $ grunt serve

The base app will now run as it would with the usual ``manage.py runserver`` but with live reloading and Sass compilation enabled.

To get live reloading to work you'll probably need to install an `appropriate browser extension`_

.. _appropriate browser extension: http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-


Run Unit Tests
--------------

::

    python manage.py test

Front-end Application
---------------------

We use bower to manage the Front-end dependencies. The project already has a compiled and minified version of the dependencies. So you only need to run it when adding new dependencies.

::

    npm -g install bower
    bower install

Path of front-end libraries: /bower_components
