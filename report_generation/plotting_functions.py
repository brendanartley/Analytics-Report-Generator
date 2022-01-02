import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from PIL import Image
import warnings
import requests
import query_data

warnings.filterwarnings("ignore", category=DeprecationWarning)
plt.rcParams.update({'font.size': 22})

def shot_scatter_plot(df, rink_image_fname, event, legend_labels, colors, out_fname):
    """
    Given a list of parameters, creates shot plot and saves 
    image to temporary file before being added to report.
    """
    #read data
    df.loc[df['x_coordinate'] >= 0, 'y_coordinate',] = -1*df["y_coordinate"]
    df.loc[df['x_coordinate'] >= 0, 'x_coordinate',] = -1*df["x_coordinate"]

    rink_img = plt.imread(rink_image_fname)

    #plot data
    plt.figure(figsize=(10,10))
    plt.scatter(df.loc[df['event'] == event]["x_coordinate"], df.loc[df['event'] == event]["y_coordinate"], c=colors[0], s=100, zorder=3)
    plt.scatter(df.loc[df['event'] != event]["x_coordinate"], df.loc[df['event'] != event]["y_coordinate"], c=colors[1], s=100, zorder=1)
    plt.imshow(rink_img, cmap="gray", extent=[-100, 100, -42.5, 42.5])
    plt.xlim(left=-100, right=0)
    plt.ylim(bottom=-42.5, top=42.5)
    plt.legend(legend_labels, prop={'size': 22})
    plt.axis('off')

    #need to add os call that checks if the file exists, and create DIR if not
    plt.savefig('./{}.png'.format("./tmp/" + out_fname), dpi=300, bbox_inches='tight')
    pass

def shot_pie_plot(df, event, legend_labels, colors, out_fname):

    #preprocess data
    if event == "Goal":
        goal_pct = round(len(df.loc[df['event'] == event]["x_coordinate"])/len(df), 3)*100
        sa = 180
    else:
        goal_pct = round(len(df.loc[df['event'] != event]["x_coordinate"])/len(df), 3)*100
        sa = 270

    #pie plot figure
    sizes = [goal_pct, 100-goal_pct]
    explodes = [0.25, 0]
    plt.figure(figsize=(10,10))
    patches, texts, _ = plt.pie(sizes, explode=explodes, autopct='%1.1f%%',shadow=True, startangle=sa, colors=colors)
    plt.legend(patches, legend_labels, loc="best", prop={'size': 22})
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    if event == "Goal":
        plt.title("Shot Scored?")
    else:
        plt.title("Shot on Net?")
    
    #save figure
    plt.savefig('./{}.png'.format("./tmp/" + out_fname), dpi=300, bbox_inches='tight')
    pass

def by_period_bar_plot(df, event, color, out_fname):
    """
    Given a dataframe, returns a matplotlib bar plot of
    the number of goals scored each period
    """
    if event != "Goals" and event != "Shots":
        sys.exit(" ---------- Invalid Event: {} ---------- ".format(event))

    #processing data
    if event == "Goals":
        goal_dict = dict(df.loc[(df["event"] == "Goal") & (df["period"].isin([1,2,3]))]["period"].value_counts().sort_index())
    else:
        goal_dict = dict(df.loc[df["period"].isin([1,2,3])]["period"].value_counts().sort_index())
    
    #creating figure
    plt.figure(figsize=(10,5))
    plt.bar(goal_dict.keys(), goal_dict.values(), color = color, width = 0.4, tick_label=[1,2,3], zorder=3)

    #remove ticks and borders
    plt.tick_params(bottom=False, left=False)
    for i, spine in enumerate(plt.gca().spines):
        if i != 2:
            plt.gca().spines[spine].set_visible(False)
        
    #labels / grid
    plt.gca().yaxis.grid(zorder=0)  
    plt.xlabel("Period")
    plt.ylabel(event)
    plt.title(event + " by Period")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    #save figure
    plt.savefig('./tmp/{}.png'.format(out_fname), dpi=300, bbox_inches='tight')
    pass

def rankings_hbar_plot(data2, out_fname):
    """
    Given player statistics rankings for the season,
    creates a horizontal bar plot.

    - Need to modify function to take a data format other than nested array
    """

    def sort_rankings(data):
        """
        Given list of rankings, returns sorted array
        """
        l = [] 
        res = []
        for i, val in enumerate(data):
            l.append([i, int(val[1][:-2])])
        l = sorted(l, key = lambda x: x[1], reverse=True)
        for val in l:
            res.append([data2[val[0]][0][4:], data2[val[0]][1]])
        return res[::-1]

    data2 = sort_rankings(data2)
    data = {"Stat": [x[0] for x in data2], "Rank": [x[1] for x in data2]}

    df = pd.DataFrame(data, index = data["Stat"])
    fig, ax = plt.subplots(figsize=(5,18))

    #range - #1f77b4 --> #aec7e8
    colors = ['#297db8','#3382bb','#3e88bf','#488ec3',
            '#5294c7','#5c99ca','#679fce','#71a5d2','#7baad5',
            '#85b0d9','#8fb6dd','#9abce1','#a4c1e4']

    p1 = ax.barh(data["Stat"], data["Rank"], color = colors)
    ax.set_title('Regular Season Rankings\n', loc='right')
    ax.margins(x=0.1, y=0)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.invert_yaxis()

    for rect, label in zip(ax.patches, [x[1] for x in data2]):
        height = rect.get_y() + (rect.get_height() / 2) + 0.15
        width = rect.get_width() + rect.get_x() + 1
        ax.text(
            width, height, label, ha="left", va="bottom"
        )

    plt.savefig('./tmp/{}.png'.format(out_fname), dpi=300, bbox_inches='tight')

def convert_pngs_to_jpegs(fpath = "./tmp"):
    """
    Given a directory, converts all .png images
    to JPEG's
    """
    for img in os.listdir(fpath):
        if img[-4:] == ".png":
            Image.open('{}/{}'.format(fpath, img)).convert('RGB').save('{}/{}.jpg'.format(fpath, img[:-4]), 'JPEG', quality=95)
            os.remove('{}/{}'.format(fpath, img))
    pass

def get_player_image(player_id, fpath =  "./tmp"):
    """
    Downloads player image for title page
    of the report
    """
    url = 'https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{}@2x.jpg'.format(player_id)
    r = requests.get(url, stream=True)
    if r.ok:
        Image.open(r.raw).save(fpath + "/player.jpg", 'JPEG', quality=95)
    pass

def check_tmp_directory():
    """
    Checks if the temporary directory has already been created
    """
    if os.path.isdir("./tmp") and len(os.listdir("./tmp")) != 0:
        sys.exit(" ERROR:\n - Delete \"./tmp\" contents to continue -")
    else:
        if not os.path.isdir("./tmp"):
            os.mkdir("./tmp")
    pass

if __name__ == "__main__":

    # check_tmp_directory()
    print(" --- Generating Plots --- ")

    player_df = query_data.player_df
    rank_list = query_data.rank_list

    rink_im = "/Users/brendanartley/dev/Sports-Analytics/imgs/simple_rink_grey.jpg"

    goal_colors = ["#88B4AA", "#e0ddbd"]
    on_net_colors = ["#e0ddbd", "#77A6C0"]

    #scatter plot rink imgs
    shot_scatter_plot(player_df, rink_im, event="Goal", legend_labels=["Goal", "No Goal"], colors = goal_colors, out_fname="rink_image1")
    shot_scatter_plot(player_df, rink_im, event="Missed Shot", legend_labels=["Missed Net", "On Net"], colors = on_net_colors[::-1], out_fname="rink_image2")

    #pie plot imgs
    shot_pie_plot(player_df, event="Goal", legend_labels=["Goal", "No Goal"], colors = goal_colors, out_fname="pie_plot1")
    shot_pie_plot(player_df, event="Missed Shot", legend_labels=["On Net", "Missed Net"], colors = on_net_colors, out_fname="pie_plot2")

    #rank plot
    rankings_hbar_plot(rank_list, out_fname = "rank_hbar_plot1")

    get_player_image(player_id=8481535, fpath =  "./tmp")
    convert_pngs_to_jpegs(fpath = "./tmp")