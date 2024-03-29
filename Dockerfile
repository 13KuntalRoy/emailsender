# base image
FROM python:3.9.10

#maintainer
LABEL Author="Kuntal"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED=1

RUN mkdir /code

#switch to /app directory so that everything runs from here
WORKDIR /code

#copy the app code to image working directory
COPY ./ /code/

#let pip install required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
