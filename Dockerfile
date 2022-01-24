FROM python:3.9-slim-buster


# set working directory
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

# install python dependencies
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# add app
COPY . .
