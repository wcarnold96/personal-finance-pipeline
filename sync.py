import os
import plaid
import json
import boto3
from datetime import datetime, timezone

from plaid.model.transactions_sync_request import TransactionsSyncRequest

from plaid_client import client

try:
    with open("tokens.json", "r") as f:
        data = json.load(f)
except:
    print("Unable to load access_tokens")

s3 = boto3.client('s3')
today = datetime.now().date()
ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
for item_id in data:
    lines = []
    has_more = True
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
                lines.append(json.dumps(record, default=str))

        has_more = response['has_more']

        cursor = response['next_cursor']
        data[item_id]['cursor'] = cursor

    s3.put_object(Bucket=os.getenv("S3_BUCKET"), Key=f"raw/transactions/sync_date={today}/transactions-{item_id}-{ts}.jsonl", Body="\n".join(lines)) 
with open("tokens.json", "w") as f:
    json.dump(data, f, indent=2)

