import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from COUNTRY import STATES

with open("states_daily.json", "r") as read_file:
    data = json.load(read_file)["states_daily"]

data = pd.DataFrame(data)
data = data.apply(pd.to_numeric, errors='ignore')

dates = list(data["date"].drop_duplicates())
data["date"] = pd.to_datetime(data['date'])

state = "tt"
data = data.loc[:, [state, "status", "date"]]
color = ["Blue", "Red", "Green",]

X = range(len(dates))
i = 0
fig, ax = plt.subplots()


for status, st_data in data.groupby("status"):
    Y = st_data[state]
    ax.plot(X, Y, "-ok", Color=color[i], label=status, markersize=5)
    i += 1

def update_annot(date, x_pos, y_pos):
    annot.xy = (x_pos, y_pos)
    text = "{}, {}".format(date, y_pos)
    annot.set_text(text)


def no_annot():
    annot.set_visible(False)
    fig.canvas.draw_idle()


def hover(event):
    x_pos, y_pos = event.xdata, event.ydata # date, case
    if x_pos:
        if int(x_pos) - x_pos <= 1 and int(x_pos) in X:
            # date as number exists
            date = dates[int(x_pos)]
            update_annot(date, int(x_pos), y_pos)
            annot.set_visible(True)
            fig.canvas.draw_idle()
            return
    no_annot()

plt.legend()
annot = ax.annotate(
    "",
    xy=(0, 0),
    xytext=(20, 20),
    textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w"),
    arrowprops=dict(arrowstyle="->"),
)
annot.set_visible(False)
plt.legend(loc="upper left")
fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()

