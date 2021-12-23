import pandas as pd
import matplotlib.pyplot as plt
import sys

plt.rcParams.update({'font.size': 22})

def shot_scatter_plot(data_fname, image_fname, event, legend_labels, out_fname):
    """
    Given a list of parameters, creates shot plot and saves 
    image to temporary file before being added to report.
    """
    #read data
    df = pd.read_csv(data_fname, header=0)
    img = plt.imread(image_fname)

    #plot data
    plt.figure(figsize=(10,10))
    plt.scatter(df.loc[df['event'] == event]["x_coordinate"], df.loc[df['event'] == event]["y_coordinate"], c="#00205B")
    plt.scatter(df.loc[df['event'] != event]["x_coordinate"], df.loc[df['event'] != event]["y_coordinate"], c="#D32717")
    plt.imshow(img, cmap="gray", extent=[-100, 100, -42.5, 42.5])
    plt.xlim(left=-100, right=0)
    plt.ylim(bottom=-42.5, top=42.5)
    plt.legend(legend_labels, prop={'size': 20})
    plt.axis('off')

    #need to add os call that checks if the file exists, and create DIR if not
    plt.savefig('./{}.png'.format(out_fname), dpi=300, bbox_inches='tight')
    pass

def shot_pie_plot(data_fname, event, legend_labels, out_fname, switch=False):

    #read data
    df = pd.read_csv(data_fname, header=0)

    if not switch:
        goal_pct = round(len(df.loc[df['event'] == event]["x_coordinate"])/len(df), 3)*100
    else:
        goal_pct = round(len(df.loc[df['event'] != event]["x_coordinate"])/len(df), 3)*100


    sizes = [goal_pct, 100-goal_pct]
    colors = ["#FFAE49", "#44B7C2"]
    explodes = [0.25, 0]
    plt.figure(figsize=(10,10))
    plt.pie(sizes, labels=legend_labels, explode=explodes, shadow=True, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #save plot
    plt.savefig('./{}.png'.format(out_fname), dpi=300, bbox_inches='tight')
    pass

if __name__ == "__main__":
    out_fname = sys.argv[1]

    data_fname = "/Users/brendanartley/dev/Sports-Analytics/raw_data/player_sample/sample.csv"
    event = "Goal"
    legend_labels = ["Goal", "Non-Goal"]
    shot_pie_plot(data_fname, event, legend_labels, out_fname)

    event = "Missed Shot"
    legend_labels = ["On-Net", "Missed-Net"]
    out_fname = sys.argv[1]
    shot_pie_plot(data_fname, event, legend_labels, "test_image4", True)

    # data = "/Users/brendanartley/dev/Sports-Analytics/raw_data/player_sample/sample.csv"
    # im = "/Users/brendanartley/dev/Sports-Analytics/imgs/simple_rink_grey.jpg"
    # event = "Goal"
    # legend_labels = ["Goal", "No-Goal"]
    # out_fname = "test_image"

    # shot_scatter_plot(data, im, event, legend_labels, "test_image")

    # data = "/Users/brendanartley/dev/Sports-Analytics/raw_data/player_sample/sample.csv"
    # im = "/Users/brendanartley/dev/Sports-Analytics/imgs/simple_rink_grey.jpg"
    # event = "Missed Shot"
    # legend_labels = ["Missed Net", "On Net"]
    # out_fname = "test_image2"

    # shot_scatter_plot(data, im, event, legend_labels, "test_image2")