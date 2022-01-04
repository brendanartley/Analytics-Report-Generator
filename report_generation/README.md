## Report Generation

`data_query.py`

The data query script contains the pyspark script that starts a spark session, and filters data by the player_id and season. The sript returns a pandas dataframe, a couple short arrays, and a dictionary. These are used to create that plots that are included in the report.

`plotting_functions.py`

This script contains the custom Matplotlib functions used the generate the plots in the report
