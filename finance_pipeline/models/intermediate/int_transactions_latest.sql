with latest as ( 
    select *,
    row_number() over (partition by transaction_id order by sync_timestamp desc) as rn 
    from {{ ref('stg_transactions') }}
)
select
  transaction_id,
  account_id,
  amount,
  date,
  authorized_date,
  name,
  merchant_name,
  pending,
  pending_transaction_id,
  payment_channel,
  item_id,
  institution,
  change_type,
  sync_timestamp
from latest
where rn = 1
and change_type != 'removed';
