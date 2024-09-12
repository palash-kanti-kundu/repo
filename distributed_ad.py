from pyspark.sql import SparkSession

from statsforecast.core import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS

from pyspark.sql.functions import col, lit

spark = SparkSession.builder.getOrCreate()
sdf = spark.read.option("header", True).csv('/opt/spark-data/time_series_data.csv')

df=sdf.select(col("Date").alias("ds"), lit("Generated_Random").alias("unique_id"), col("Value").alias("y").cast('double'))

sf = StatsForecast(models = [AutoETS()], freq = 'D')

fcst = sf.forecast(df=df, h=5, level=[90], fitted = True)
fcst.write.mode("append").format("csv").option("header", "true").save("/opt/spark-data/forecast")
insample_forecasts = sf.forecast_fitted_values()
insample_forecasts.head()

anomalies = insample_forecasts[(insample_forecasts['y'] >= insample_forecasts['AutoETS-hi-90']) | (insample_forecasts['y'] <= insample_forecasts['AutoETS-lo-90'])]
anomalies.write.mode("append").format("csv").option("header", "true").save("/opt/spark-data/anomalies")
