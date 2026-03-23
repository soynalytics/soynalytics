#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import mysql.connector
import matplotlib.pyplot as plt
# DESCRIPTION: retrieve info from db and scatter plot with matplotlib
# TODO

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Plot scraped data from soyscraper")
	parser.add_argument("sql", nargs = "+", help = "sql commands, must have exactly 2 fields, first field MUST be `time` in unix seconds")
	parser.add_argument("--credentials", action = "store", type = str, default = "$SOYSCRAPERDBCREDS", help = "Env to load credentials from")
	# parser.add_argument("--llabel", action = "store", type = str, help = "X label")
	parser.add_argument("--rlabel", action = "store", type = str, help = "Y label")
	parser.add_argument("--title", action = "store", type = str, help = "Title / description")
	args = parser.parse_args()

	with open(os.path.expanduser(os.path.expandvars(args.credentials))) as fp:
		credentials = json.load(fp)

	connection = mysql.connector.connect(
			host = credentials["host"],
			port = credentials["port"],
			user = credentials["username"],
			password = credentials["password"],
			database = credentials["database"],
			buffered = True
	)
	cursor = connection.cursor()

	colours = [
		"steelblue",
		"red",
		"lime",
		"gold",
		"magenta",
		"orangered",
		"darkcyan"
	]
	# input(args.sql)
	fig, ax = plt.subplots()

	cursor.execute(args.sql[0])
	res = [datetime.datetime.fromtimestamp(i[0]) for i in cursor.fetchall()]
	# print(f"Y length: {len(res)}")

	ax.plot(
		res, # date
		[eval(f"{i.hour}.{round((i.minute / 60) * 100)}") for i in res], # hour
		linestyle = "None",
		marker = "o",
		color = colours[0]
	)

	ax.set_xlabel("Date", fontsize = 14)
	ax.set_ylabel("Hour", fontsize = 12)

	if len(args.sql) > 1:
		for index, command in enumerate(args.sql[1:]):
			cursor.execute(command)
			res = [datetime.datetime.fromtimestamp(i[0]) for i in cursor.fetchall()]
			# print(f"Y2 length: {len(res)}")

			newAx = ax.twinx()
			newAx.plot(
				res, # date
				[eval(f"{i.hour}.{round((i.minute / 60) * 100)}") for i in res], # hour
				linestyle = "None",
				marker = "o",
				color = colours[index + 1]
			)

			if index == 0:
				# print(args.rlabel)
				newAx.set_ylabel(args.rlabel, fontsize = 12)

	plt.title(args.title)
	plt.gcf().autofmt_xdate()
	plt.grid(True)
	plt.show()

	cursor.close()
	connection.close()
