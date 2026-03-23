# StatsCLI

StatsCLI consists of 3 main programs.

premade.py is the easiest to use as all of its command are premade (hence the name)

however if you want to write more indepth and complicated commands you can use line.py or scatter.py

for line graphs and scatter plots respectively 

## premade.py 

### usage:

run the program and the first argument is the command you want to run

the following arguments will be passed as variables to this command

### extra arguments: 

`--ltime` exclude entries >= {ltime} (can be unix seconds or %Y-%m-%dT%H:%M:%SZ format)

`--rtime` exclude entries <= {rtime} (can be unix seconds or %Y-%m-%dT%H:%M:%SZ format)

`--limit` limit amount of entries

### example commands:

plot pph /soy/: `python premade.py pph soy`

plot pph and num posters 
