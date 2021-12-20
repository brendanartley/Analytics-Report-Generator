import pandas as pd
import matplotlib.pyplot as plt

def shot_scatter_plot(data_fname, image_fname, event, legend_labels, out_fname):
    """
    Given a list of parameters, saves images to temporary file
    before being added to report.
    """
    df = pd.read_csv(data_fname, header=0)
    img = plt.imread(image_fname)
    plt.figure(figsize=(10,10))
    plt.scatter(df.loc[df['event'] == event]["x_coordinate"], df.loc[df['event'] == event]["y_coordinate"], c="#00205B")
    plt.scatter(df.loc[df['event'] != event]["x_coordinate"], df.loc[df['event'] != event]["y_coordinate"], c="#D32717")
    plt.imshow(img, cmap="gray", extent=[-100, 100, -42.5, 42.5])
    plt.xlim(left=-100, right=0)
    plt.ylim(bottom=-42.5, top=42.5)
    plt.legend(legend_labels, prop={'size': 10})

    #remove grid/axis from plot
    plt.axis('off')

    #need to add os call that checks if the file exists, and create DIR if not
    plt.savefig('./{}.png'.format(out_fname), dpi=300, bbox_inches='tight')
    pass

def shot_pie_plot(data_fname, image_fname, event, legend_labels, out_fname):
    #NEED TO INCREASE BRIGHTNESS OF IMAGE
    pass

data = "/Users/brendanartley/dev/Sports-Analytics/raw_data/player_sample/sample.csv"
im = "/Users/brendanartley/dev/Sports-Analytics/imgs/simple_rink_grey.jpg"
event = "Goal"
legend_labels = ["Goal", "No-Goal"]
out_fname = "test_image"

shot_scatter_plot(data, im, event, legend_labels, out_fname)

data = "/Users/brendanartley/dev/Sports-Analytics/raw_data/player_sample/sample.csv"
im = "/Users/brendanartley/dev/Sports-Analytics/imgs/simple_rink_grey.jpg"
event = "Missed Shot"
legend_labels = ["Missed Net", "On Net"]
out_fname = "test_image2"

shot_scatter_plot(data, im, event, legend_labels, out_fname)