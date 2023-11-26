# pull official base image
FROM python:slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat iproute2

# copy project
COPY . /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod u+x /usr/src/app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
