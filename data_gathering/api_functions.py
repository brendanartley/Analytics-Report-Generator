import sys
import grequests
import constants
import json
from tqdm import tqdm

def game_ids(just_regular_season, filter_by_team, season_start, season_end, teamId):
    """
    inputs ..(just_regular_season=True, filter_by_team=False, season_start=20112012, season_end=20202021, teamId=23)

    Given starting season, ending season, and regular season boolean, team boolean, team id etc..
    Returns all the game_ids for specified the season range as an array/list.

    season_start -> season_end is inclusive
    """
    #variables
    id_array = []
    url = constants.NHL_STATS_API
    endpoint = "api/v1/schedule/?season="

    #urls
    urls = ["{}{}{}{}".format(url, endpoint, i, i+1) for i in range(season_start // 10000, (season_end // 10000)+1)]
    if just_regular_season:
        urls = [val + "&gameType=R" for val in urls]
    if filter_by_team:
        urls = [val + "&teamId={}".format(teamId) for val in urls]

    #making requests - 10x faster than simple requests
    reqs = (grequests.get(u) for u in urls)
    responses = grequests.map(reqs)

    #Fetch ID's from json
    for r in responses:
        if r.ok:
            d = r.json()
            for i in range(len(d["dates"])):
                for j in range(len(d["dates"][i]["games"])):
                    id_array.append(d["dates"][i]["games"][j]["gamePk"])

    return id_array


def simple_season_game_stats(fname, season_start=20112012, season_end=20202021, just_regular_season=True):
    """
    Returns scores, teams, shots for every game from 2010-2020.
    Output's json format into the raw folder

    Note that asynchronous requests not implemented here
    """

    #URL format
    url = constants.NHL_STATS_API
    endpoint = "api/v1/schedule/?expand=schedule.linescore&season="

    #Creating each individual URL
    urls = ["{}{}{}{}".format(url, endpoint, i, i+1) for i in range(season_start // 10000, (season_end // 10000)+1)]
    if just_regular_season:
        urls = [x + "&gameType=R" for x in urls]

    #making requests
    reqs = (grequests.get(u) for u in urls)
    responses = grequests.map(reqs)

    with open("./raw_data/{}.json".format(fname), 'w', encoding='utf-16') as f:
        for r in responses:
            if r.ok:
                d = r.json()
                rj = {"gamePk":"",
                    "season":"",
                    "away_team_name":"",
                    "away_team_id":"",
                    "away_team_goals":"",
                    "away_shots":"",
                    "home_team_name":"",
                    "home_team_id":"",
                    "home_team_goals":"",
                    "home_shots":""
                    }

                #looping through every game in specified season
                for i in range(len(d["dates"])):
                    for j in range(len(d["dates"][i]["games"])):
                        game = d["dates"][i]["games"][j]
                        if game["status"]["abstractGameState"] == 'Final':
                            rj["gamePk"] = game["gamePk"]
                            rj["season"] = game["season"]
                            rj["away_team_name"] = game["linescore"]["teams"]["away"]["team"]["name"]
                            rj["away_team_id"] = game["linescore"]["teams"]["away"]["team"]["id"]
                            rj["away_team_goals"] = game["linescore"]["teams"]["away"]["goals"]
                            rj["away_shots"] = game["linescore"]["teams"]["away"]["shotsOnGoal"]
                            rj["home_team_name"] = game["linescore"]["teams"]["home"]["team"]["name"]
                            rj["home_team_id"] = game["linescore"]["teams"]["home"]["team"]["id"]
                            rj["home_team_goals"] = game["linescore"]["teams"]["home"]["goals"]
                            rj["home_shots"] = game["linescore"]["teams"]["home"]["shotsOnGoal"]

                            f.write(json.dumps(rj) + '\n')
        pass

def get_event_stats(game_id_array, fname):
    """
    Given a list of game ID's, returns raw event data for each game
    in a format suitable for pyspark.
    """
    #Variables
    id_array = []
    url = constants.NHL_STATS_API
    endpoint = "api/v1/game/{}/feed/live"

    #Formatting URL's
    urls = [url + endpoint.format(date) for date in game_id_array]

    #Making requests - 10x faster than simple requests
    reqs = (grequests.get(u) for u in tqdm(urls, desc="API Requests"))
    responses = grequests.map(reqs)

    #NEED TO COMPLETE FUNCTION HERE - Need to explore raw data
    # ex - 'https://statsapi.web.nhl.com/api/v1/game/2020020663/feed/live'
    #
    # d["liveData"]["plays"]["allPlays"][10]
    #  - need to find out who was on the ice for each event
    rj = {}

    with open("../raw_data/{}.json".format(fname), 'w', encoding='utf-16') as f:
        for resp in tqdm(responses, desc="Writing Data to Disk"):
            if resp.ok:
                d = resp.json()

                if "gamePk" in d:
                    rj["gamePk"] = d["gamePk"]
                else:
                    continue

                for val in d["liveData"]["plays"]["allPlays"]:

                    rj["event"] = val["result"]["event"]
                    rj["periodTime"] = val["about"]["periodTime"]
                    rj["dateTime"] = val["about"]["dateTime"]
                    rj["period"] = val["about"]["period"]
                    
                    #on ice-coordinates
                    if len(val["coordinates"]) == 2:
                        rj["x_coordinate"] = val["coordinates"]["x"]
                        rj["y_coordinate"] = val["coordinates"]["y"]
                    else:
                        rj["x_coordinate"] = None
                        rj["y_coordinate"] = None

                    #players involved, can be up to 4
                    if "players" in val:
                        num_players = len(val["players"])
                        if num_players > 4:
                            print(" ---------- Event > 4 Players?? ---------- ")
                        for i in range(4):
                            if i < num_players:
                                rj["p{}_id".format(i+1)] = val["players"][i]["player"]["id"]
                                rj["p{}_type".format(i+1)] = val["players"][i]["playerType"]
                                rj["p{}_name".format(i+1)] = val["players"][i]["player"]["fullName"]
                            else:
                                rj["p{}_id".format(i+1)] = None
                                rj["p{}_type".format(i+1)] = None
                                rj["p{}_name".format(i+1)] = None

                    else:
                        for i in range(4):
                            rj["p{}_id".format(i+1)] = None
                            rj["p{}_type".format(i+1)] = None
                            rj["p{}_name".format(i+1)] = None

                    #team-id if relevant
                    if "team" in val:
                        rj["team_id"] = val["team"]["id"]
                    else:
                        rj["team_id"] = None
                    
                    #write output to JSON
                    f.write(json.dumps(rj) + '\n')
            else:
                print("{}".format(resp.status_code))
        
        #remove the '/n' at the end of JSON file
        f.seek(0, 2) # seek to end of file
        f.seek(f.tell() - 2, 0)  # seek to the second last char of file
        f.truncate()

def main(output):
    #canucks_game_ids = game_ids(True, True, season_start=20112012, season_end=20202021, teamId=23)
    get_event_stats([2020020663], fname=output)
    return
    
if __name__ == '__main__':
    output = sys.argv[1]
    main(output)