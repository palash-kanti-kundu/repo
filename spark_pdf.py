from statsforecast.core import StatsForecast
from statsforecast.models import (AutoARIMA, AutoETS)
from statsforecast.utils import generate_series
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.getOrCreate()

sf = StatsForecast(
    models=[AutoETS(season_length=7)],
    freq='D',
)

n_series = 4
horizon = 7

sdf = spark.read.option("header", True).csv('data/PRICE_AND_DEMAND_201801_NSW1.csv')

df=sdf.select(col("SETTLEMENTDATE").alias("ds"), 
              col("SETTLEMENTDATE").alias("unique_id"), 
              col("TOTALDEMAND").alias("y").cast('double'))
'''
df=sdf.select(lit("date").alias("unique_id"), 
              col("date").alias("ds"), 
              col("meantemp").alias("y").cast('double'))
'''
sf.forecast(df=df, h=horizon, level=[90]).show(5)