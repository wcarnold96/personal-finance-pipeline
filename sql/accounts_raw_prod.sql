CREATE EXTERNAL TABLE `accounts_raw_prod`(
  `institution` string,
  `institution_id` string,
  `sync_timestamp` string,
  `item_id` string,
  `account` struct<account_id:string,balances:struct<available:double,current:double,limit:double,iso_currency_code:string,unofficial_currency_code:string>,mask:string,name:string,official_name:string,type:string,subtype:string,apy:double,holder_category:string>)
PARTITIONED BY (
  `sync_date` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://YOUR_BUCKET_NAME/raw/accounts/env=production'
TBLPROPERTIES (
  'projection.enabled'='true',
  'projection.sync_date.format'='yyyy-MM-dd',
  'projection.sync_date.range'='YOUR_FIRST_SYNC_DATE, NOW',
  'projection.sync_date.type'='date',
  'storage.location.template'='s3://YOUR_BUCKET_NAME/raw/accounts/env=production/sync_date=${sync_date}')
