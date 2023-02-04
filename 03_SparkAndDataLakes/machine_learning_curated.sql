CREATE EXTERNAL TABLE IF NOT EXISTS 
`stedi`.`machine_learning_curated` (
  `user` string,
  `timestamp` timestamp,
  `x` float,
  `y` float,
  `z` float,
  `sensorreadingtime` bigint,
  `serialnumber` string,
  `distancefromobject` int
)
ROW FORMAT SERDE 
'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 
'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION 's3://stedi-lh/machine_learning/'
TBLPROPERTIES ('classification' = 'parquet');
