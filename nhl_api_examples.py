import sys
import requests

def main():
    '''
    See documentation on NHL API by Drew Hynes.

    https://gitlab.com/dword4/nhlapi/-/tree/master
    '''
    #Startpoint for every API request
    url = 'https://statsapi.web.nhl.com/'

    #team stats example (ID: 23 - Canucks, Franchise ID: 20) 
    endpoint = "api/v1/teams/23"

    #player stats example (ID: 8474568 - Luke Schenn)
    endpoint = "api/v1/people/8474568"

    #game ID example (ID: )
    endpoint = "api/v1/game/2020020018/feed/live"

    r = requests.get(url + endpoint)
    return
    
if __name__ == '__main__':
    main()