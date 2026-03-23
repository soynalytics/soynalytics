#!/usr/bin/env python3
import argparse
import datetime
import json
import os
# test cmds
# python line.py "SELECT time,pph FROM pph WHERE board = \"soy\" and time >= 1773370800" "SELECT time,count FROM jewdar WHERE time >= 1773370800"
# python line.py "SELECT time,content FROM statistics WHERE time >= 1773370800"
# python line.py "SELECT time,posters FROM statistics WHERE time >= 1773370800"
# python line.py "SELECT time,score FROM rtl" "SELECT time,voters FROM rtl"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Run premade commands")
	parser.add_argument("args", nargs = "+", help = "Command and arguments to give to program")
	parser.add_argument("--limit", action = "store", type = int, help = "Limit results by count")
	parser.add_argument("--ltime", action = "store", help = "Limit by time >= (unix timestamp or YYYY-MM-DDTHH:MM:SSZ)") # %Y-%m-%dT%H:%M:%SZ
	parser.add_argument("--rtime", action = "store", help = "Limit by time <= (unix timestamp or YYYY-MM-DDTHH:MM:SSZ)") # %Y-%m-%dT%H:%M:%SZ
	parser.add_argument("--commands", action = "store", type = str, default = "commands.json", help = "JSON file with commands")
	args = parser.parse_args()

	convertTime = lambda time : int(time) if time.isdigit() else round(datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ").timestamp())

	with open(args.commands) as fp:
		allCommands = json.load(fp)

	key = args.args[0]

	if key not in allCommands.keys():
		print(f"Unknown command: `{key}`")
		exit()

	command = allCommands[key]
	commands = command[2]
	arguments = args.args[1:]
	where = True

	if (argCount := len(arguments)) != command[1]:
		print(f"Expected {command[1]} arguments recieved {argCount} arguments")
		exit()

	if [command for command in commands if "WHERE" not in command] != [] and any((args.ltime, args.rtime)): # fix commands that dont have `WHERE`
		commands = [command + " WHERE" for command in commands]
		where = False

	# TODO do all this in one loop instead
	# add in ltime limit
	if args.ltime is not None:
		ltime = convertTime(args.ltime)
		commands = [command + f"{' AND' if where else ''} time >= {ltime}" for command in commands]

	# add in rtime limit
	if args.rtime is not None:
		rtime = convertTime(args.rtime)
		commands = [command + f"{' AND' if where else ''} time <= {rtime}" for command in commands]

	# add in count limit
	commands = [command + " ORDER BY time DESC" for command in commands]

	if args.limit is not None:
		commands = [command + f" LIMIT {args.limit}" for command in commands]

	# print(commands + command[3])
	command = f"python3 {'line' if command[0] == 0 else 'scatter'}.py " + " ".join((list(f"\"{command}\"" for command in commands) + command[3]))

	if len(args.args) > 1: # if we need arguments from user then format them here
		command = command.format(*args.args[1:])

	print(f"Running: `{command}`")
	os.system(command)
