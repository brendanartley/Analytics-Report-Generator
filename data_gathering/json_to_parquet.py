import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import os

from pyspark.sql import SparkSession, functions, types #type:ignore

def main():
    """
    Converting the JSON Data to Parquet 
    """
    inputs = "./raw_data/"

    for file in os.listdir(inputs):
        if file[-5:] == ".json":
            df = spark.read.json(inputs + file)
            df.write.parquet("./raw_data/parquet/{}".format(file[:-5]))
    pass

if __name__ == '__main__':
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()