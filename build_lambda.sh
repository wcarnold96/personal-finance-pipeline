#!/bin/bash
set -e
rm -rf package lambda.zip
pip install -t package/ -r requirements-lambda.txt
cp sync.py plaid_client.py package/
cd package && zip -r ../lambda.zip . && cd ..
echo "Built lambda.zip"
