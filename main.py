import json
import matplotlib.pyplot as plt
from datetime import datetime
from COUNTRY import STATES


def date_to_int(date):
    today = datetime.now()
    day_of_year = (date - datetime(today.year, 1, 1)).days + 1
    return day_of_year


with open("states_daily.json", "r") as read_file:
    data = json.load(read_file)["states_daily"]

dates = list(set([d["date"] for d in data]))
dates = sorted(
    	dates,
    	key=lambda date: datetime.strptime(date, "%d-%b-%y"),
		)  # %b - abbreviated months
dates_to_integer = [date_to_int(datetime.strptime(date, "%d-%b-%y")) for date in dates]
int_to_date = dict(zip(dates_to_integer, dates))
total_confirmed_each_day = {}
date = 0
for i in range(0, len(data), 3):
    total_confirmed_each_day[dates[date]] = int(data[i]["tt"])  # 'tt' -> TOTAL
    date += 1


def update_annot(x_pos):
    y_pos = dataset[x_pos]
    annot.xy = (x_pos, y_pos)
    text = "{}, {}".format(int_to_date[x_pos], y_pos)
    annot.set_text(text)


def no_annot():
    annot.set_visible(False)
    fig.canvas.draw_idle()


def hover(event):
    x_pos, y_pos = event.xdata, event.ydata
    if x_pos:
        if int(x_pos) in X:
            if abs(int(y_pos) - dataset[int(x_pos)]) <= 500:
                update_annot(int(x_pos))
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                no_annot()
        else:
            no_annot()
    else:
        no_annot()


fig, ax = plt.subplots()
X, Y = dates_to_integer, list(total_confirmed_each_day.values())
dataset = dict(zip(X, Y))
plt.plot(X, Y, "-ok", Color="Blue", label="Current", markersize=5)
annot = ax.annotate(
    "",
    xy=(0, 0),
    xytext=(20, 20),
    textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w"),
    arrowprops=dict(arrowstyle="->"),
)
annot.set_visible(False)
plt.legend(loc="upper center")
fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()
