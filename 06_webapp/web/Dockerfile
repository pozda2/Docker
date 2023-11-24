FROM python:3-alpine
RUN python -m pip install --upgrade pip
COPY webroot /usr/src/app

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN chmod a+x /usr/src/app/gunicorn.sh
EXPOSE 5000

ENTRYPOINT ["/bin/sh", "/usr/src/app/gunicorn.sh"]

