import os
import plaid
import json
import boto3
from datetime import datetime, timezone, UTC
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid_client import client, env

s3 = boto3.client('s3')
ssm = boto3.client('ssm')
dynamodb = boto3.client('dynamodb')

def get_tokens(ssm):
    response = ssm.get_parameters_by_path(
        Path=f"/finance-pipeline/{env}/plaid/",
        Recursive=True,
        WithDecryption=True
    )
    tokens = {}
    for param in response['Parameters']:
        item_id = param['Name'].split('/')[-2]
        tokens[item_id] = param['Value']
    if not tokens:
        raise RuntimeError(f"No access tokens found for env '{env}'")
    return tokens


def get_cursor(item_id, dynamodb):
    response = dynamodb.get_item(
        TableName='finance-pipeline-cursors',
        Key={'item_id': {'S': f"{env}#{item_id}"}}
        )
    if 'Item' not in response:
        return None
    return response['Item']['cursor']['S']

def lambda_handler(event, context):

    today = datetime.now(UTC).date()
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bucket = os.environ["S3_BUCKET"]

    tokens = get_tokens(ssm)

    for item_id in tokens:
        cursor = get_cursor(item_id, dynamodb)

        account_lines = []
        accounts_request = AccountsGetRequest(access_token=tokens[item_id])
        accounts_response = client.accounts_get(accounts_request)
        institution_id = accounts_response['item']['institution_id']
        institution = accounts_response['item']['institution_name']

        for account in accounts_response['accounts']:
            record = {
                'item_id': item_id,
                'sync_timestamp': ts,
                'institution': institution,
                'institution_id': institution_id,
                'account': account.to_dict()
            }
            account_lines.append(json.dumps(record, default=str))

        s3.put_object(
            Bucket=bucket,
            Key=f"raw/accounts/env={env}/sync_date={today}/accounts-{item_id}-{ts}.jsonl",
            Body="\n".join(account_lines)
        )

        lines = []
        has_more = True
        while has_more:
            if cursor:
                request = TransactionsSyncRequest(
                    access_token=tokens[item_id],
                    cursor=cursor
                )
            else:
                request = TransactionsSyncRequest(
                    access_token=tokens[item_id]
                )
            response = client.transactions_sync(request)
            for change_type in ('added', 'modified', 'removed'):
                for txn in response[change_type]:
                    record = {
                        'item_id': item_id,
                        'change_type': change_type,
                        'sync_timestamp': ts,
                        'institution': institution,
                        'transaction': txn.to_dict()
                    }
                    lines.append(json.dumps(record, default=str))
            has_more = response['has_more']
            cursor = response['next_cursor']
        if lines:
            s3.put_object(
                Bucket=bucket,
                Key=f"raw/transactions/env={env}/sync_date={today}/transactions-{item_id}-{ts}.jsonl",
                Body="\n".join(lines)
            )
        dynamodb.put_item(
            TableName='finance-pipeline-cursors',
            Item={
                'item_id': {'S': f"{env}#{item_id}"},
                'cursor': {'S': cursor},
                'last_sync_timestamp': {'S': ts},
                'record_count': {'N': str(len(lines))}
            }
        )
    return {"statusCode": 200, "itemsSynced": len(tokens)}

if __name__ == "__main__":
    print(lambda_handler({}, None))
