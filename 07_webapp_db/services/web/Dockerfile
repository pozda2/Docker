# pull official base image
FROM python:slim-buster

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# copy project
COPY . /usr/src/app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod a+x /usr/src/app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/bin/sh","/usr/src/app/entrypoint.sh"]
