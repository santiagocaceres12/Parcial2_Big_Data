CREATE EXTERNAL TABLE scraping_results(
title string,
category string,
link string
)
PARTITIONED BY (newspaper string, year string, month string, day string)        
ROW FORMAT DELIMITED
fields terminated by ","
escaped by "\\"
lines terminated by "\n"
location "s3://resultadosnewscsv/news/final/"
TBLPROPERTIES ("skip.header.line.count"="1");

MSCK REPAIR TABLE scraping_results;
