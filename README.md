# Sports Analytics

Working with the NHL API to see what I can predict with the data.

See Documentation on this here. [Stats Api Docs](https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md#configurations)


Current Idea: Create Analytics Report using FPDF
- include stats leaders for across a time period (month, year)
    - split defenders + offensive?
- include Corsi rating

## Ex ID's

Hoglander - 8481535
Canucks - 23

### Notes

- I would like to only work with data in the past 10 years. Due to the vast differences in the game from 20 years ago till now, it is probably for the best.

- Use tableau for a custom rink visualization?

- Need to add a more concrete way of checking inputs. 
    ie. Specify teamID, season start and end on program call.

### Potential Questions?

- Can I predict who will win a playoff series?
- Which players are undervalued?  <-- I like this one.
- Who is going to win the cup?
- What will be the score of the game?
- Where are specific players scoring from?
- Where are goalies getting scored on?
- What makes a Stanley Cup winning team different from other teams?
- Predict attendance in an Arena?
- What makes the best powerplay's most effective?

example GameID = 2020020018

### Dumping JSON Data to File

import json
with open('data.json', 'w') as f:
    json.dump(data, f)

### Grequests over Requests

Given that the NHL_API server does not have any limitations, we can leverage the power of asynchronous requests and get information much faster. 

Asynchronous requests basically create requests at the same time to reduce the time we are spending waiting for responses.