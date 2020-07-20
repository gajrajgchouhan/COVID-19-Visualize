import json
import matplotlib.pyplot as plt
import datetime
from collections import Counter
from COUNTRY import STATES

def date_to_int(date):
	today = datetime.datetime.now()
	day_of_year = (date - datetime.datetime(today.year, 1, 1)).days + 1
	return day_of_year

def int_to_date(integer):
	return dates[len(dates) - integer]

with open("states_daily.json", "r") as read_file:
	data = json.load(read_file)['states_daily']

dates = list(set([d['date'] for d in data]))
dates = sorted(dates, key=lambda date: datetime.datetime.strptime(date, '%d-%b-%y')) # %b - abbreviated months
dates_to_integer = [date_to_int(datetime.datetime.strptime(date, '%d-%b-%y')) for date in dates]
total_confirmed_each_day = {}
date = 0
for i in range(0, len(data), 3):
	# for state in STATES:
	# 	cases = int(data[i][state])
	# 	print(f"Date : {dates[date]}, State : {state}, Confirmed Cases : {cases}")
	# 'tt' is TOTAL
	total_confirmed_each_day[dates[date]] = int(data[i]['tt'])
	date += 1

fig,ax = plt.subplots()
X, Y = dates_to_integer, list(total_confirmed_each_day.values())
dataset = dict(zip(X, Y))
plt.plot(X, Y, '-ok', Color='Blue', label='Current',
		 markersize=5)
annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
					bbox=dict(boxstyle="round", fc="w"),
					arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)
def update_annot(x_pos):
	y_pos = dataset[x_pos]
	annot.xy = (x_pos, y_pos)
	text = "{}, {}".format(int_to_date(x_pos), y_pos)
	annot.set_text(text)
	# annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
	# annot.get_bbox_patch().set_alpha(0.4)

def no_annot():
	annot.set_visible(False)
	fig.canvas.draw_idle()

def hover(event):
	x_pos, y_pos = event.xdata, event.ydata
	if x_pos:
		if int(x_pos) in X:
			if (abs(int(y_pos) - dataset[int(x_pos)]) <= 500):
					# print(int(x_pos), int(y_pos))
					update_annot(int(x_pos))
					annot.set_visible(True)
					fig.canvas.draw_idle()
			else: no_annot()
		else: no_annot()
	else: no_annot()
		
	# vis = annot.get_visible()
	# if event.inaxes == ax:
	#     cont, ind = sc.contains(event)
	#     if cont:
	#         update_annot(ind)
	#         annot.set_visible(True)
	#         fig.canvas.draw_idle()
	#     else:
	#         if vis:
	#             annot.set_visible(False)
	#             fig.canvas.draw_idle()

plt.legend(loc="upper center")
fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()