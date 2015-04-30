#! /usr/bin/env python
# coding=utf8

# __Author__: Yixuan Li (yl2363@cornell.edu), Zheng Yao (zy87@cornell.edu)


import json
import pickle
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
from collections import defaultdict
import os




def load_data(file_path):
	copy = pickle.load(open(file_path, "rb" ))

	return copy


def load_data_multi(file_path):
	files = os.listdir(file_path)
	print files
	data = []
	for pickle_file in files:
		rumor_data = pickle.load(open(file_path+pickle_file, "rb" ))
		data += rumor_data

	return data


def view_time_distr(data):
	# visualize the distribution of the view times of rumors
	view_time = []
	for r in data:
		#print r
		print r.values()[0]
		temp = int(r.values()[0][4])
		view_time.append(temp)
	print "max:",np.array(view_time).max()

	plt.hist(view_time,bins=np.arange(0, 800, 4),color="#9ecae1")
	plt.xlabel("Rumor report view times")
	plt.ylabel('Frequency')
	plt.show()         # disp visualization


def report_freq_distr(data):
	report_freq = defaultdict(int)
	rumor_poster_freq = defaultdict(int)
	entry = 0
	for r in data:
		print r.values()[0][2].split('/')
		reporter_id = r.values()[0][2].split('/')[-1]
		rumor_poster_id = r.values()[0][3].split('/')[-1]
		report_freq[reporter_id] += 1
		rumor_poster_freq[rumor_poster_id] += 1
		entry += 1

	max_report_time = np.array(report_freq.values()).max()
	print "number of unique reporters:",len(report_freq.values())
	print "maximum reporting frequency:", max_report_time
	threshold = int(max_report_time*0.05)
	print threshold
	print np.sort(np.array(report_freq.values()))[::-1][:100]
	max_report_keys = [(k,v) for k,v in report_freq.items() if v>30]
	print "user id who has the maximum report time:", max_report_keys
	#print "sum",np.sum(np.array(report_freq.values()))
	print "number of unique rumor spreaders:",len(rumor_poster_freq.values())
	print "maximum spreader frequency:", np.array(rumor_poster_freq.values()).max()
	n, bins, patches = plt.hist(report_freq.values(),bins=np.arange(1, 200, 1),color="#9ecae1")
	plt.xlabel("Historical rumor report times (total unique reporters: {})".format(len(report_freq.values())))
	plt.ylabel('Frequency')
	plt.show()         # disp visualization


	# pie chart
	# The slices will be ordered and plotted counter-clockwise.
	labels = '1 time', '2-10 times','>10 times'
	sizes = [n[0],np.sum(n[1:9]),len(report_freq.values())-n[0]-np.sum(n[1:9])]
	print sizes
	colors = ['yellowgreen', 'gold', 'lightskyblue']
	colors = ["#9ecae1", 'gold', 'yellowgreen']
	explode = (0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
	        autopct='%1.1f%%', shadow=True, startangle=90)
	plt.title("Historical rumor report times (total unique reporters: {})".format(len(report_freq.values())))
	plt.show()         # disp visualization


	n, bins, patches = plt.hist(rumor_poster_freq.values(),bins=np.arange(1, 10, 1),color="#9ecae1")
	print n
	plt.show()

	# pie chart
	# The slices will be ordered and plotted counter-clockwise.
	labels = 'once', '2-4 times','>4 times'
	sizes = [n[0],n[1]+n[2]+n[3],entry-n[0]-n[2]-n[1]-n[3]]
	colors = ["#9ecae1", 'gold', 'yellowgreen']
	explode = (0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
	        autopct='%1.1f%%', shadow=True, startangle=90)
	plt.title("Times being reported for spreading rumors (total unique spreaders: {})".format(len(rumor_poster_freq.values())))
	plt.show()         # disp visualization




def report_per_month(data):
	month_freq = defaultdict(int)
	for r in data:
		date = r.values()[0][5]
		print date
		month = date.split('-')[0] + '-' + date.split('-')[1]
		month_freq[month] += 1

	sorted_keys = np.sort(np.array(month_freq.keys()))
	print sorted_keys

	sorted_val = [month_freq[v] for v in sorted_keys]

	# http://matplotlib.org/examples/api/barchart_demo.html
	n = len(sorted_val)
	
	width = 0.6  
	ind = np.arange(n) 

	fig, ax = plt.subplots() 
	
	ax.bar(ind,sorted_val,width,color="#9ecae1")
	ax.set_xticks(ind)
	ax.set_xticklabels(sorted_keys,rotation=70)
	ax.set_ylabel('Report frequency')
	ax.set_title('# of total rumor report cases each month')
	plt.show()


####################################################################################

if __name__ == '__main__':

	fname = "first_100_page"
	fpath = "rumor_meta_data/"
	# load rumor meta data
	#rumor = load_data(fname)
	
	rumor = load_data_multi(fpath)
	
	report_per_month(rumor)


	view_time_distr(rumor)

	report_freq_distr(rumor)

	
