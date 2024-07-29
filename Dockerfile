FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 7755

ENV FLASK_APP=core/server.py
# RUN rm core/store.sqlite3
RUN flask db upgrade -d core/migrations/


CMD [ "bash", "run.sh"]