# -*- coding: robot -*-

*** Variables ***

${Hostname}     127.0.0.1
${PORT}         55001
${SERVER}       http://${HOSTNAME}:${PORT}
${BROWSER}      googlechrome
${HOME_URL}     ${SERVER}/


*** Settings ***

Documentation   Django Robot Tests
Library         Selenium2Library  timeout=10  implicit_wait=0
Library         DjangoLibrary  ${HOSTNAME}  ${PORT}  path=../../  manage=../../manage.py  settings=config.settings.local
Suite Setup     Start Django and open browser
Suite Teardown  Stop Django and close browser


*** Keywords ***

Start Django and open browser
  Start Django
  Open Browser  ${SERVER}  ${BROWSER}

Stop Django and close browser
  Close Browser
  Stop Django

Browser is open to home page
  Go To  ${HOME_URL}


*** Test Cases ***

Can open page
  Given browser is open to home page
  When Wait until page contains element  id=mainNav
  Then Page should contain  Ekratia 
