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

run the `soyjak_schema.sql` or `soyjak.sql` file with whatever database engine you like (i've tried mariadb and mysql and both work fine although you may have to tweak the script accordingly)

make sure you create your user and give it the required privileges.

