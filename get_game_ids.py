import sys
import requests
import constants

def get_game_ids(id=23, season=20192020, just_regular_season=True):
    """
    Given a team id and season id, returns all the game ID's of a particular season.

    Default is Canucks, 2019-2020 season, regular games.
    """
    id_array = []
    url = constants.NHL_STATS_API
    endpoint = "/schedule/?expand=schedule.linescore&teamId={}&season={}".format(id, season)

    if just_regular_season:
        endpoint += "&gameType=R"

    r = requests.get(url + endpoint)
    if r.ok:
        d = r.json()
        try:
            for i in range(len(d["dates"])):
                id_array.append(d["dates"][i]["games"][0]["gamePk"])
        except:
            print(" -- Error Extracting GameID's from JSON -- ")

    return id_array

def main():
    game_ids = get_game_ids()
    print(game_ids)
    return
    
if __name__ == '__main__':
    main()