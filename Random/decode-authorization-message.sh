#!/bin/bash

enc_msg=$1

aws sts decode-authorization-message --encoded-message $enc_msg | jq '.["DecodedMessage"]'  | sed 's/\\"/"/g' | sed 's/^"//' | sed 's/"$//' | jq


