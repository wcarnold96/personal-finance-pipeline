import os
import plaid
import json
from datetime import datetime, timezone

from plaid.model.transactions_sync_request import TransactionsSyncRequest

from plaid_client import client

try:
    with open("tokens.json", "r") as f:
        data = json.load(f)
except:
    print("Unable to load access_tokens")

ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
for item_id in data:
    has_more = True
    with open(f"transactions-{ts}.jsonl", "a") as t:
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

            for change_type in ('added', 'modified', 'removed'):
                for txn in response[change_type]:
                    record = {'item_id': item_id, 'change_type': change_type, 'sync_timestamp': ts, 'institution': data[item_id]['institution'], 'transaction': txn.to_dict()}
                    t.write(json.dumps(record, default=str) + "\n")

            has_more = response['has_more']

            cursor = response['next_cursor']
            data[item_id]['cursor'] = cursor

with open("tokens.json", "w") as f:
    json.dump(data, f, indent=2)

