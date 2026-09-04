select count(*)
from {{ ref('fct_daily_cash_flow') }}
having count(*) = 0
