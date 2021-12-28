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

### Notes / To Do

- PNG's seem to be loading much slower than JPG files, maybe I can convert the matplotlib figures to jpg or jpeg when I am creating the plots?
    - Image.open('pie_plot1.png').convert('RGB').save('pie_plot1.jpg','JPEG')

- Add an intro page (or maybe add to the cover page)
    - URL to fetch player headshot images 
        - https://cms.nhl.bamgrid.com/images/headshots/current/168x168/8481535@3x.jpg

- "ALL" the api functions should be updated so that we only have to call them once and then store the data in some sort of database/parquet.
    - Call all years at once ("not by single season")

    - We are only doing the current single season/single player way for small data samples.

- Need to make sure shot PCT is correct. Use player stats rather than my calculations

- Need to modify rankings plotting function to take a data format other than nested array

- I would like to only work with data in the past 10 years. Due to the vast differences in the game from 20 years ago till now, it is probably for the best.

- Need to add a more concrete way of checking inputs. 
    ie. Specify teamID, season start and end on program call.

- Change color and size of dots on scatter plot
- Maybe Include titles on the bar and pie plots

- Use plotly or some other decent table visuluzlization library to visualize some data?

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

### Photopea

Used [PhotoPea](https://www.photopea.com/) to make edits to the rink image. Great in-browser, free tool that is like photoshop.


### Shot Selection Data

df3 = df.where((df["p1_id"] == 8481535) & (df["p1_type"].isin(["Shooter","Scorer"]))).select("x_coordinate","y_coordinate","event","p1_id","p1_name","period","periodTime")
df3.coalesce(1).write.option("header", True).csv("./player_sample2", mode="overwrite")