select 
  transaction.transaction_id as transaction_id,
  transaction.account_id as account_id,
  transaction.amount as amount,
  cast(transaction.date as date) as date,
  cast(transaction.authorized_date as date) as authorized_date,
  transaction.name as name,
  transaction.merchant_name as merchant_name,
  transaction.pending as pending,
  transaction.pending_transaction_id as pending_transaction_id,
  transaction.payment_channel as payment_channel,
  item_id as item_id,
  institution as institution,
  change_type as change_type,
  sync_timestamp as sync_timestamp

from {{ source('finance', 'transactions_raw') }}
