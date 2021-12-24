import pandas as pd
import matplotlib.pyplot as plt
import sys

plt.rcParams.update({'font.size': 22})

def shot_scatter_plot(data_fname, rink_image_fname, event, legend_labels, out_fname):
    """
    Given a list of parameters, creates shot plot and saves 
    image to temporary file before being added to report.
    """
    #read data
    df = pd.read_csv(data_fname, header=0)
    rink_img = plt.imread(rink_image_fname)

    #plot data
    plt.figure(figsize=(10,10))
    plt.scatter(df.loc[df['event'] == event]["x_coordinate"], df.loc[df['event'] == event]["y_coordinate"], c="#00205B")
    plt.scatter(df.loc[df['event'] != event]["x_coordinate"], df.loc[df['event'] != event]["y_coordinate"], c="#D32717")
    plt.imshow(rink_img, cmap="gray", extent=[-100, 100, -42.5, 42.5])
    plt.xlim(left=-100, right=0)
    plt.ylim(bottom=-42.5, top=42.5)
    plt.legend(legend_labels, prop={'size': 22})
    plt.axis('off')

    #need to add os call that checks if the file exists, and create DIR if not
    plt.savefig('./{}.png'.format(out_fname), dpi=300, bbox_inches='tight')
    pass

def shot_pie_plot(data_fname, event, legend_labels, out_fname, color_switch=False):

    #read data
    df = pd.read_csv(data_fname, header=0)
    goal_pct = round(len(df.loc[df['event'] == event]["x_coordinate"])/len(df), 3)*100

    #plot colors
    colors = ["#FFAE49", "#44B7C2"]
    if color_switch:
        colors = colors[::-1]

    #pie plot figure
    sizes = [goal_pct, 100-goal_pct]
    explodes = [0.25, 0]
    plt.figure(figsize=(10,10))
    plt.pie(sizes, labels=legend_labels, explode=explodes, shadow=True, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 22})
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    #save figure
    plt.savefig('./{}.png'.format(out_fname), dpi=300, bbox_inches='tight')
    pass

def by_period_bar_plot(data_fname, event, color,  out_fname):
    """
    Given a dataframe, returns a matplotlib bar plot of
    the number of goals scored each period
    """
    if event != "Goals" and event != "Shots":
        sys.exit(" ---------- Invalid Event: {} ---------- ".format(event))

    #loading + processing data
    df = pd.read_csv(data_fname, header=0)
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
    plt.ylabel("All " + event)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    #save figure
    plt.savefig('./{}.png'.format(out_fname), dpi=300, bbox_inches='tight')
    pass


if __name__ == "__main__":
    #out_fname = sys.argv[1]

    data_fname = "/Users/brendanartley/dev/Sports-Analytics/raw_data/player_sample2/sample2.csv"
    rink_im = "/Users/brendanartley/dev/Sports-Analytics/imgs/simple_rink_grey.jpg"

    # #scatter plot rink imgs
    # shot_scatter_plot(data_fname, rink_im, event="Goal", legend_labels=["Goal", "No Goal"], out_fname="rink_image1")
    # shot_scatter_plot(data_fname, rink_im, event="Missed Shot", legend_labels=["Missed Net", "On Net"],  out_fname="rink_image2")

    # #pie plot imgs
    # shot_pie_plot(data_fname, event="Goal", legend_labels=["Goal", "Non Goal"], out_fname="pie_plot1")
    shot_pie_plot(data_fname, event="Missed Shot", legend_labels=["Missed Net", "On Net"], out_fname="pie_plot2", color_switch=True)

    # #Bar plot imgs
    # by_period_bar_plot(data_fname, event="Goals", color="#44B7C2", out_fname="bar_plot1")
    # by_period_bar_plot(data_fname, event="Shots", color="#FFAE49", out_fname="bar_plot2")