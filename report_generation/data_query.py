import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types #type:ignore

# add more functions as necessary

def query(p_id, season):

    print(str(p_id) + " - " + str(season))

    #start spark session
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext

    #player events
    df = spark.read.parquet("./raw_data/parquet/livefeed_p2")
    player_df = (df.where(
                 (df["p1_id"] == p_id) & 
                 (df["p1_type"].isin(["Shooter","Scorer"])) & 
                 (df["season"] == season))
                  .select("x_coordinate","y_coordinate","event","p1_id","p1_name","period","periodTime"))

    #player rankings
    rank_df = spark.read.parquet("./raw_data/parquet/regularSeasonStatRankings_p2")
    rank_df = rank_df.where((rank_df["p_id"] == p_id) & (rank_df["season"] == season))
    rank_list = [[col,rank_df.take(1)[0][col]] for col in rank_df.columns if col not in ["p_id", "season"]]

    #player goal stats
    goal_stats_df = spark.read.parquet("./raw_data/parquet/goalsByGameSituationStats_p2")
    goal_stats_df = goal_stats_df.where((goal_stats_df["p_id"] == p_id) & (goal_stats_df["season"] == season))
    goal_stats_list = [[col,goal_stats_df.take(1)[0][col]] for col in goal_stats_df.columns if col not in ["p_id", "season"]]

    #player other stats
    p_stats_df = spark.read.parquet("./raw_data/parquet/statsSingleSeason_p2")
    p_stats_df =  p_stats_df.where((p_stats_df["p_id"] == p_id) & (p_stats_df["season"] == season))

    stats = ['assists', 'goals', 'games', 'hits', 'powerPlayPoints', 
             'penaltyMinutes', 'faceOffPct', 'blocked', 'plusMinus', 
            'points', 'shifts', 'timeOnIcePerGame', 'evenTimeOnIcePerGame', 
            'shortHandedTimeOnIcePerGame', 'powerPlayTimeOnIcePerGame']

    player_stats_list = [[col,p_stats_df.take(1)[0][col]] for col in p_stats_df.columns if col in stats]

    #player information
    p_info_df = spark.read.parquet("./raw_data/parquet/yearByYear_p2")
    p_info_df = (p_info_df.where((p_info_df["p_id"] == p_id) & 
                                          (p_info_df["season"] == season))
                                           .orderBy(p_info_df["team_num_this_season"], ascending=False))
    player_info = {col:p_info_df.take(1)[0][col] for col in p_info_df.columns}

    return player_df.toPandas(), rank_list, goal_stats_list, player_info, player_stats_list

# if __name__ == 'query_data':
#     spark = SparkSession.builder.appName('example code').getOrCreate()
#     assert spark.version >= '3.0' # make sure we have Spark 3.0+
#     spark.sparkContext.setLogLevel('WARN')
#     sc = spark.sparkContext
#     player_df, rank_list = main()