FROM ubuntu:latest

RUN apt-get update -y && apt-get install python3-pip -y

COPY . /ssrf-bug

WORKDIR ssrf-bug

RUN pip3 install -r requirements.txt

CMD python3 app.py