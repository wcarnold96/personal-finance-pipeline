CREATE EXTERNAL TABLE `transactions_raw`(
  `change_type` string COMMENT 'from deserializer', 
  `sync_timestamp` string COMMENT 'from deserializer', 
  `institution` string COMMENT 'from deserializer', 
  `item_id` string COMMENT 'from deserializer', 
  `transaction` struct<transaction_id:string,account_id:string,amount:double,date:string,authorized_date:string,name:string,merchant_name:string,pending:boolean,pending_transaction_id:string,payment_channel:string,personal_finance_category:struct<primary:string,detailed:string,confidence_level:string,version:string>> COMMENT 'from deserializer')
PARTITIONED BY ( 
  `sync_date` string)
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://wcarnold-finance-lake/raw/transactions'
TBLPROPERTIES (
  'last_modified_by'='hadoop', 
  'last_modified_time'='1788528837', 
  'projection.enabled'='true', 
  'projection.sync_date.format'='yyyy-MM-dd', 
  'projection.sync_date.range'='2026-09-01, NOW', 
  'projection.sync_date.type'='date', 
  'storage.location.template'='s3://wcarnold-finance-lake/raw/transactions/sync_date=${sync_date}', 
  'transient_lastDdlTime'='1788528837');
