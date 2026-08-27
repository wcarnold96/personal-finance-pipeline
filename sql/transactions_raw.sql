CREATE EXTERNAL TABLE IF NOT EXISTS transactions_raw ( 
  change_type string,
  sync_timestamp string,
  institution string,
  transaction struct<
    transaction_id:string,
    account_id:string,
    amount:double,
    date:string,
    authorized_date:string,
    name:string,
    merchant_name:string,
    pending:boolean,
    pending_transaction_id:string,
    payment_channel:string,
    personal_finance_category:struct<
      primary:string,
      detailed:string,
      confidence_level:string,
      version:string
    >
  >
)
PARTITIONED BY (item_id string, sync_date string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://<insert-your-bucket-here>';
