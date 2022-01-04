# Data Gathering 

`api_functions.py`

This is the meat and potatoes of the data gathering process. This script contains all the API requests and JSON filtering used when sending requests to the API.

`constants.py`

Contains the constants that always prepend the endpoint for each request.

`json_to_parquet.py`

Given a directory name, converts all JSON files in that directory to a parquet format using Pyspark

`nhl_api_examples.py`

Provides a few simple example of how to make a request to the NHL API.

See more comprehensive endpoint examples here --> [NHL Api Docs](https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md#configurations)


