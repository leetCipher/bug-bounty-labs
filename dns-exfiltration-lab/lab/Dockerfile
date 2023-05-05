FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install python3 -y

RUN apt-get install python3-pip -y

RUN apt-get install dnsutils -y

RUN apt-get install curl -y

RUN apt-get install base58 -y

RUN apt-get install iptables -y

COPY . /app

WORKDIR app

RUN pip3 install -r requirements.txt

RUN chmod +x iptables-rules.sh

CMD /app/iptables-rules.sh

