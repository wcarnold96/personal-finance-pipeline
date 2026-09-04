select
  account.account_id as account_id,
  account.balances.available as available_balance,
  account.balances."current" as current_balance,
  account.balances."limit" as balance_limit,
  account.balances.iso_currency_code as iso_currency_code,
  account.mask as mask,
  account."name" as account_name,
  account.official_name as official_name,
  account."type" as account_type,
  account.subtype as subtype,
  account.apy as apy,
  account.holder_category as holder_category,
  institution as institution,
  institution_id as institution_id,
  sync_timestamp as sync_timestamp,
  item_id as item_id

from {{ source('finance', 'accounts_raw') }}
