#!/bin/bash

# setup iptables rules
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -F
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --sport 80 -j ACCEPT
iptables -A INPUT -p tcp --match multiport --dports 49335:49354 -j ACCEPT
iptables -A OUTPUT -p tcp --match multiport --sports 49335:49354 -j ACCEPT
iptables -P INPUT DROP	
iptables -P OUTPUT DROP
iptables -I INPUT -p udp -j ACCEPT
iptables -I OUTPUT -p udp -j ACCEPT

# run server
python3 app.py
