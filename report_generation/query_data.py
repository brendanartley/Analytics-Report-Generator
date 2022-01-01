import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types #type:ignore

# add more functions as necessary

def main(inputs, output):

    df = spark.read.parquet("./raw_data/parquet/livefeed_real")

    player_df = (df.where(
                 (df["p1_id"] == 8481535) & 
                 (df["p1_type"].isin(["Shooter","Scorer"])))
                  .select("x_coordinate","y_coordinate","event","p1_id","p1_name","period","periodTime"))
    
    player_df.coalesce(1).write.option("header", True).csv("./tmp/player_sample", mode="overwrite")

    df2 = spark.read.parquet("./raw_data/parquet/regularSeasonStatRankings_real")
    df2

if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main(inputs, output)