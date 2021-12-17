import sys
import grequests
import constants
import json

def game_ids(just_regular_season=True, filter_by_team=False, teamId=23, season_start=20112012, season_end=20202021):
    """
    Given starting season, ending season, and regular season boolean, team boolean, team id..
    return all the game_ids for the time range as a python list.
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

def get_player_stats(game_id_array=[2020020663, 2020020664, 2020020195]):
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
    reqs = (grequests.get(u) for u in urls)
    responses = grequests.map(reqs)

    #NEED TO COMPLETE FUNCTION HERE - Need to explore raw data
    # ex - 'https://statsapi.web.nhl.com/api/v1/game/2020020663/feed/live'
    #
    # d["liveData"]["plays"]["allPlays"][10]
    #  - need to find out who was on the ice for each event

    pass

def main(output):
    return
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = "simple_stats"
    main(output)