import sys
import grequests
import constants
import json
from tqdm import tqdm
import re

def get_game_ids(just_regular_season, filter_by_team, season_start, season_end, teamId=23):
    """
    inputs example ..(just_regular_season=True, filter_by_team=False, season_start=20112012, season_end=20202021, teamId=23)

    Given starting season, ending season, and regular season boolean, team boolean, team id etc..
    Returns all the game_ids for specified the season range as an array/list.

    - season_start and season_end are inclusive
    """
    #log
    print("\n -- Getting Game ID's -- \n")

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
    reqs = (grequests.get(u) for u in tqdm(urls, desc="API Requests"))
    responses = grequests.map(reqs)

    #Fetch ID's from json
    for r in tqdm(responses, desc="Collecting List"):
        if r.ok:
            d = r.json()
            for i in range(len(d["dates"])):
                for j in range(len(d["dates"][i]["games"])):
                    id_array.append(d["dates"][i]["games"][j]["gamePk"])

    return id_array

def get_all_player_ids_in_range(season_start, season_end):
    """
    Given a season, returns a list of all the players
    on an NHL roster that year.
    """
    #log
    print("\n -- Getting Players in Season Range -- \n")

    #constants
    url = constants.NHL_STATS_API
    endpoint = "api/v1/teams?expand=team.roster&season="
    urls = ["{}{}{}{}".format(url, endpoint, i, i+1) for i in range(season_start // 10000, (season_end // 10000)+1)]
    players = set()

    #Doing API calls in batches
    for b in tqdm(range(0, len(urls), 100), desc="Iterating Batches"):
        batch = urls[b:b+100]

        #making requests
        reqs = (grequests.get(u) for u in batch)
        responses = grequests.map(reqs)

        #writing data to file
        for r in responses:
            if r.ok:
                d = r.json()
                for i in range(len(d['teams'])):
                    team_data = d['teams'][i]
                    for player in team_data['roster']['roster']:
                        if "person" in player and "id" in player["person"]:
                            players.add(player["person"]["id"])

    return list(players)

def simple_game_stats(fname, season_start, season_end, just_regular_season=True):
    """
    Returns scores, teams, shots for every game from 2010-2020.
    Output's json format into the raw folder
    """
    #log
    print("\n -- Getting Simple Game Stats -- \n")

    #URL format
    fname = "linescore_" + fname
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

        rj = {"gamePk":"",
              "season":"",
              "away_name":"",
              "away_id":"",
              "away_goals":"",
              "away_shotsOnGoal":"",
              "home_name":"",
              "home_id":"",
              "home_goals":"",
              "home_shotsOnGoal":""
              }

        stats_tracked = ["goals", "shotsOnGoal"]
        team_info = ["id", "name"]

        for r in tqdm(responses, desc="Writing Data to Disk"):
            if r is not None and r.ok and r.json() is not None:
                d = r.json()

                #looping through every game in specified season
                for i in range(len(d["dates"])):
                    for j in range(len(d["dates"][i]["games"])):
                        game = d["dates"][i]["games"][j]
                        if game["status"]["abstractGameState"] == 'Final':
                            if "gamePk" and "season" in game:
                                rj["gamePk"] = game["gamePk"]
                                rj["season"] = game["season"]

                                for event in stats_tracked:
                                    if event in game["linescore"]["teams"]["away"] and game["linescore"]["teams"]["home"]:
                                        rj["away_{}".format(event)] = game["linescore"]["teams"]["away"][event]
                                        rj["home_{}".format(event)] = game["linescore"]["teams"]["home"][event]
                                    else:
                                        continue

                                for item in team_info:
                                    if item in game["linescore"]["teams"]["away"]["team"] and game["linescore"]["teams"]["home"]["team"]:
                                        rj["away_{}".format(item)] = game["linescore"]["teams"]["away"]["team"][item]
                                        rj["home_{}".format(item)] = game["linescore"]["teams"]["home"]["team"][item]

                                f.write(json.dumps(rj) + '\n')

        f.seek(0, 2) # seek to end of file
        f.seek(f.tell() - 2, 0)  # seek to the second last char of file
        f.truncate()
    pass

def get_all_game_event_stats(game_id_array, fname):
    """
    Given a list of game ID's, returns raw event data for each game
    in a format suitable for pyspark.
    """
    #log
    print("\n -- Getting All Game Events -- \n")

    #Variables
    fname = "livefeed_" + fname
    url = constants.NHL_STATS_API
    endpoint = "api/v1/game/{}/feed/live"

    #Formatting URL's
    urls = [url + endpoint.format(date) for date in game_id_array]

    with open("./raw_data/{}.json".format(fname), 'w', encoding='utf-16') as f:
        #Doing API calls in batches
        for b in tqdm(range(0, len(urls), 100), desc="Iterating Batches"):
            batch = urls[b:b+100]

            #Making requests - 10x faster than simple requests
            reqs = (grequests.get(u) for u in batch)
            responses = grequests.map(reqs)

            rj = {}

            for resp in responses:
                if resp is not None and resp.ok and resp.json() is not None:
                    d = resp.json()

                    if "gamePk" in d:
                        rj["gamePk"] = d["gamePk"]
                    else:
                        continue

                    rj["season"] = d["gameData"]['game']['season']

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
            
        #remove the '/n' at the end of written JSON file
        f.seek(0, 2) # seek to end of file
        f.seek(f.tell() - 2, 0)  # seek to the second last char of file
        f.truncate()

def get_players_season_goal_stats(player_id_array, season_start, season_end, fname, just_regular_season=True):
    """
    Given an array of player_id's and a season,
    returns the goal statistics for each player
    in JSON format.
    """
    #log
    print("\n -- Getting Player Goal Stats -- \n")

    #constants
    fname = "goalsByGameSituationStats_" + fname
    url = constants.NHL_STATS_API
    endpoint = "api/v1/people/{}/stats?stats=goalsByGameSituation&season="
    urls = []

    url_format = ["{}{}{}{}".format(url, endpoint, i, i+1) for i in range(season_start // 10000, (season_end // 10000)+1)]
    if just_regular_season:
        url_format = [x + "&gameType=R" for x in url_format]

    goal_stats_tracked = [
              'goalsInFirstPeriod',
              'goalsInSecondPeriod',
              'goalsInThirdPeriod',
              'gameWinningGoals',
              'emptyNetGoals',
              'shootOutGoals',
              'shootOutShots',
              'goalsTrailingByOne',
              'goalsTrailingByThreePlus',
              'goalsWhenTied',
              'goalsLeadingByOne',
              'goalsLeadingByTwo',
              'goalsLeadingByThreePlus',
              'penaltyGoals',
              'penaltyShots',
              ]

    #Creating each individual URL
    for p_id in player_id_array:
        for url in url_format:
            urls.append(url.format(p_id))

    with open("./raw_data/{}.json".format(fname), 'w', encoding='utf-16') as f:
        rj = {}

        #Doing API calls in batches
        for b in tqdm(range(0, len(urls), 100), desc="Iterating Batches"):
            batch = urls[b:b+100]

            #making requests
            reqs = (grequests.get(u) for u in batch)
            responses = grequests.map(reqs)

            for r in responses:
                if r is not None and r.ok and r.json() is not None:
                    d = r.json()
                    rj['p_id'] = int(re.findall(r'[//][0-9]+', r.url)[0][1:])
                    rj['season'] = re.findall(r'\d+', r.url)[-1]
                    if len(d["stats"][0]["splits"]) != 0:
                        for ev in goal_stats_tracked:
                            if ev in d["stats"][0]["splits"][0]["stat"]:
                                rj[ev] = d["stats"][0]["splits"][0]["stat"][ev]
                            else:
                                rj[ev] = 0
                        f.write(json.dumps(rj) + '\n')

        #remove the '/n' at the end of written JSON file
        f.seek(0, 2) # seek to end of file
        f.seek(f.tell() - 2, 0)  # seek to the second last char of file
        f.truncate()

def get_players_season_general_stats(player_id_array, season_start, season_end, fname, just_regular_season=True):
    """
    Given an array of player_id's and a season,
    returns the general statistics for each player
    in JSON format.
    """
    #log
    print("\n -- Getting Player General Stats -- \n")

    
    #constants
    fname = "statsSingleSeason_" + fname
    url = constants.NHL_STATS_API
    endpoint = "api/v1/people/{}/stats?stats=statsSingleSeason&season="
    urls = []
    
    url_format = ["{}{}{}{}".format(url, endpoint, i, i+1) for i in range(season_start // 10000, (season_end // 10000)+1)]
    if just_regular_season:
        url_format = [x + "&gameType=R" for x in url_format]

    stats_tracked = [
        'timeOnIce',
        'assists',
        'goals',
        'pim',
        'shots',
        'games',
        'hits',
        'powerPlayGoals',
        'powerPlayPoints',
        'powerPlayTimeOnIce',
        'evenTimeOnIce',
        'penaltyMinutes' ,
        'faceOffPct',
        'shotPct',
        'gameWinningGoals',
        'overTimeGoals',
        'shortHandedGoals',
        'shortHandedPoints',
        'shortHandedTimeOnIce',
        'blocked',
        'plusMinus',
        'points',
        'shifts',
        'timeOnIcePerGame',
        'evenTimeOnIcePerGame',
        'shortHandedTimeOnIcePerGame',
        'powerPlayTimeOnIcePerGame',
      ]

    #Creating each individual URL
    for p_id in player_id_array:
        for url in url_format:
            urls.append(url.format(p_id))

    #writing data to file
    with open("./raw_data/{}.json".format(fname), 'w', encoding='utf-16') as f:
        rj = {}

        #Doing API calls in batches
        for b in tqdm(range(0, len(urls), 100), desc="Iterating Batches"):
            batch = urls[b:b+100]

            #making requests
            reqs = (grequests.get(u) for u in batch)
            responses = grequests.map(reqs)

            for r in responses:
                if r is not None and r.ok and r.json() is not None:
                    d = r.json()
                    rj['p_id'] = int(re.findall(r'[//][0-9]+', r.url)[0][1:])
                    if len(d["stats"][0]["splits"]) != 0:
                        rj["season"] = d["stats"][0]["splits"][0]['season']
                        for ev in stats_tracked:
                            if ev in d["stats"][0]["splits"][0]["stat"]:
                                rj[ev] = d["stats"][0]["splits"][0]["stat"][ev]
                            else:
                                rj[ev] = None
                        
                        f.write(json.dumps(rj) + '\n')

        #remove the '/n' at the end of written JSON file
        f.seek(0, 2) # seek to end of file
        f.seek(f.tell() - 2, 0)  # seek to the second last char of file
        f.truncate()

def get_players_season_stat_rankings(player_id_array, season_start, season_end, fname):
    """
    Given an array of player_id's and a season,
    returns the rankings across numerous statisitcs
    for each player in a JSON format.
    """
    #log
    print("\n -- Getting Player Rankings -- \n")
    
    #constants
    fname = "regularSeasonStatRankings_" + fname
    url = constants.NHL_STATS_API
    endpoint = "api/v1/people/{}/stats?stats=regularSeasonStatRankings&season="
    urls = []

    url_format = ["{}{}{}{}".format(url, endpoint, i, i+1) for i in range(season_start // 10000, (season_end // 10000)+1)]

    stats_tracked = ['rankPowerPlayGoals',
                     'rankBlockedShots',
                     'rankAssists',
                     'rankShotPct',
                     'rankGoals',
                     'rankHits',
                     'rankPenaltyMinutes',
                     'rankShortHandedGoals',
                     'rankPlusMinus',
                     'rankShots',
                     'rankPoints',
                     'rankOvertimeGoals',
                     'rankGamesPlayed',
                    ]

    #Creating each individual URL
    for p_id in player_id_array:
        for url in url_format:
            urls.append(url.format(p_id))

    #writing data to file
    with open("./raw_data/{}.json".format(fname), 'w', encoding='utf-16') as f:
        rj = {}

        #Doing API calls in batches
        for b in tqdm(range(0, len(urls), 100), desc="Iterating Batches"):
            batch = urls[b:b+100]

            #making requests
            reqs = (grequests.get(u) for u in batch)
            responses = grequests.map(reqs)

            for r in responses:
                if r is not None and r.ok and r.json() is not None:
                    d = r.json()
                    rj['p_id'] = int(re.findall(r'[//][0-9]+', r.url)[0][1:])

                    if len(d["stats"][0]["splits"]) != 0:
                        rj["season"] = d["stats"][0]["splits"][0]['season']
                        for ev in stats_tracked:
                            if ev in d["stats"][0]["splits"][0]["stat"]:
                                rj[ev] = d["stats"][0]["splits"][0]["stat"][ev]
                            else:
                                rj[ev] = None
                        
                        f.write(json.dumps(rj) + '\n')

        #remove the '/n' at the end of written JSON file
        f.seek(0, 2) # seek to end of file
        f.seek(f.tell() - 2, 0)  # seek to the second last char of file
        f.truncate()

def main(output):

    ss = 20112012
    se = 20202021

    #get ids
    all_game_ids = get_game_ids(just_regular_season=True, filter_by_team=False, season_start=ss, season_end=se)
    all_player_ids = get_all_player_ids_in_range(season_start=ss, season_end=se)

    #game events + stats
    simple_game_stats(fname=output, season_start=ss, season_end=se, just_regular_season=True)
    get_all_game_event_stats(all_game_ids, fname=output)
    
    #player_stats
    get_players_season_goal_stats(all_player_ids, season_start=ss, season_end=se, fname=output)
    get_players_season_general_stats(all_player_ids, season_start=ss, season_end=se, fname=output)
    get_players_season_stat_rankings(all_player_ids, season_start=ss, season_end=se, fname = output)
    return
    
if __name__ == '__main__':
    output = sys.argv[1]
    main(output)