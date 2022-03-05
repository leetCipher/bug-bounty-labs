FROM ubuntu:latest

RUN apt-get update -y && apt-get install python3-pip -y

RUN apt-get update -y && apt-get install curl -y	

COPY . /lab

WORKDIR lab

RUN pip3 install -r requirements.txt

CMD python3 app.py