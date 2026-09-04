select
  format_datetime(date, 'yyyy-MM') as month,
  personal_finance_category as finance_category,
  sum(amount) as total_spend
from {{ ref('int_transactions_latest') }}
where personal_finance_category not in ('INCOME', 'TRANSFER_IN', 'TRANSFER_OUT')
group by 1, 2
