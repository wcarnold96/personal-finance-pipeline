with latest as (
    select *,
    row_number() over (partition by account_id order by sync_timestamp desc) as rn
    from {{ ref('stg_accounts') }}
)
select 
  account_id,
  available_balance,
  current_balance,
  balance_limit,
  iso_currency_code,
  mask,
  account_name,
  official_name,
  account_type,
  subtype,
  apy,
  holder_category,
  institution,
  institution_id,
  sync_timestamp,
  item_id
from latest
where rn = 1
