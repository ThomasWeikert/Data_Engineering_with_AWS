CREATE EXTERNAL TABLE `accelerometer_landing`(
  `user` string,
  `timeStamp` bigint,
  `x` float,
  `y` float,
  `z` float)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'paths'='timeStamp,user,x,y,z')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://stedi-lh/accelerometer/landing/'
TBLPROPERTIES (
  'classification'='json')
