import os
import plaid
import json

from plaid.model.transactions_sync_request import TransactionsSyncRequest

from plaid_client import client

try:
    with open("tokens.json", "r") as f:
        data = json.load(f)
except:
    print("Unable to load access_tokens")

added = []
modified = []
removed = []
has_more = True

for item_id in data:
    while has_more:
        if data[item_id]['cursor']:
            request = TransactionsSyncRequest(
                    access_token=data[item_id]['access_token'],
                    cursor=data[item_id]['cursor']
            )
        else:
            request = TransactionsSyncRequest(
                    access_token=data[item_id]['access_token']
            )
        response = client.transactions_sync(request)

        added.extend(response['added'])
        modified.extend(response['modified'])
        removed.extend(response['removed'])

        has_more = response['has_more']

        cursor = response['next_cursor']

        print(response)

