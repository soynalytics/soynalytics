# Soy Analytics

Program to collect and analyze usage data from soyjak.st

## SoyScraper

Collects information from soyjak.st

## StatsCLI

Create graphs from collected information with matplotlib

## StatsWebapp

Create graphs in an easy to use webapp

# Setup 

To setup first clone this repo: `git clone https://github.com/soynalytics/soynalytics`

make sure you have python installed and cd into `soynalytics`

then run `python3 -m pip3 install -r requirements.txt`

(its recommended to setup the SoyScraper on a dedicated server) 

## DB Setup:

run the `soyjak_schema.sql` or `soyjak.sql` file with whatever database engine you like 

(i've tried mariadb and mysql and both work fine although you may have to tweak the script accordingly)

make sure you create your user and give it the required privileges.

after you have got the database and user setup correctly, now you need to plug those credentials into the `credentials.json` file

after that you need to set the variable `$SOYSCRAPERDBCREDS` 

make sure to set the path correctly `export SOYSCRAPERDBCREDS=Path/To/soynalytics/credentials.json`

you also need to give `credentials.json` a valid `mccaptcha` cookie

to test everything is running you can cd into ScraperRunner and run `python main.py -n -v`

if everything is working you should see some sql commands run.

if you see nothing its probably not working, to verify you can `cat scraper.log` for extra info
