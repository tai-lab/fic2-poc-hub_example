FROM python:3.4.2-onbuild

RUN python setup.py develop
