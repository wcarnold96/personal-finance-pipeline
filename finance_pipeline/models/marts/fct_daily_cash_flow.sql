select 
  date,
  count(distinct(transaction_id)) as transaction_count,
  sum(case when amount <= 0 then 0 else amount end) as cash_outflow,
  abs(sum(case when amount >= 0 then 0 else amount end)) as cash_inflow,
  -sum(amount) as net_cash_flow
from {{ ref('int_transactions_latest') }}
group by date
