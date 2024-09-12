import pandas as pd
import numpy as np
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

# Not needed in pyspark
'''
spark = (
    SparkSession.builder
      .appName('learn pandas UDFs in Spark 3.2')
      .config('spark.sql.execution.arrow.pyspark.enabled', True) 
      .config('spark.sql.execution.arrow.pyspark.fallback.enabled', False)
      .getOrCreate()
)
'''

# series to scalar
@F.pandas_udf(T.DoubleType())
def average_column(col1: pd.Series) -> float:
    print("I am on it")
    return col1.mean()

sdf = spark.read.option("header", True).csv('data/PRICE_AND_DEMAND_201801_NSW1.csv')
df=sdf.select(col("SETTLEMENTDATE").alias("ds"), 
              to_date("SETTLEMENTDATE").alias("unique_id"), 
              col("TOTALDEMAND").alias("y").cast('double'))

res = df.groupby('unique_id').agg(average_column(F.col('y')).alias('average of y'))
