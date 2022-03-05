FROM ubuntu:latest

RUN apt-get update -y && apt-get install python3-pip -y

RUN apt-get install sqlite3 -y

COPY . /admin-login-bypass

WORKDIR admin-login-bypass

RUN pip3 install -r requirements.txt

CMD python3 app.py