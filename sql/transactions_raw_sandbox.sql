CREATE EXTERNAL TABLE `transactions_raw_sandbox`(
  `change_type` string,
  `sync_timestamp` string,
  `institution` string,
  `item_id` string,
  `transaction` struct<transaction_id:string,account_id:string,amount:double,date:string,authorized_date:string,name:string,merchant_name:string,pending:boolean,pending_transaction_id:string,payment_channel:string,personal_finance_category:struct<primary:string,detailed:string,confidence_level:string,version:string>>)
PARTITIONED BY (
  `sync_date` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://YOUR_BUCKET_NAME/raw/transactions/env=sandbox'
TBLPROPERTIES (
  'projection.enabled'='true',
  'projection.sync_date.format'='yyyy-MM-dd',
  'projection.sync_date.range'='YOUR_FIRST_SYNC_DATE, NOW',
  'projection.sync_date.type'='date',
  'storage.location.template'='s3://YOUR_BUCKET_NAME/raw/transactions/env=sandbox/sync_date=${sync_date}')
