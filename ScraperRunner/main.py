#!/usr/bin/env python3
import argparse
import json
import logging
import os
import time
from datetime import datetime, timedelta
from itertools import chain
# pypi
from bs4 import BeautifulSoup
import mysql.connector
from rnet import Jar, Cookie
from rnet.blocking import Client
from rnet.emulation import Emulation
from rnet.exceptions import *

DOMAIN = "https://soyjak.st" # incase domain gets taken down or changes
cInt = lambda s : int(s) if str(s).isnumeric() else str(s) # convert to int if numeric

class Scraper:
	def _getPage(self, url: str) -> str: # base get webpage using session function
		# print(url)
		r = self.client.get(url)

		if (status := r.status.as_int()) != 200:
			try:
				title = BeautifulSoup(r.text(), features = "lxml").title
			except:
				title = None

			raise StatusError(f"Request had invalid HTTP status code of `{status}` title: `{title}`")
		return r.text()

	# count retarded porn spam keyword count and log into db total number of occurences
	def jewdar(self, board: str):
		catty = self._getPage(f"{self.domain}/{board}/catalog.html").lower()
		return sum((catty.count(phrase) for phrase in self.phrases))

	def happenings(self):
		text = self._getPage(f"https://soyjakwiki.org/Happenings/{datetime.now().year}")
		s = BeautifulSoup(text, features = "lxml")

		return [li.text for li in list(chain.from_iterable([ul.find_all("li") for ul in s.find("div", class_ = "mw-content-ltr mw-parser-output").find_all("ul")]))]

	# # BEGIN
	# # def hiddenBoards(self)
	# 	# get pph data for hidden boards that dont appear on the homepage
	# # END

	def rtl(self): # nu method using wiki data cause doesnt have aggressive retarded tls fingerprinting just to get results
		text = self._getPage("https://soyjakwiki.org/RTL/Log")
		s = BeautifulSoup(text, features = "lxml")

		table = s.find("table", class_ = "wikitable sortable")
		startDate = datetime(2025, 12, 24, 21, 0, 0) # when rtl started
		c = 0

		for row in table.find_all("tr"):
			td = row.find_all("td")

			if [td.text for td in td if str(td.text).startswith("R")] == []: # skip tr rows that dont contain data rows
				continue

			yield [
				float(td[2].text.lstrip("R").split(" ")[0]),
				(lambda s : int(s) if str(s).isnumeric() else 0)(td[3].text),
				int((startDate + timedelta(c)).timestamp())
			]
			c += 1
			# print(c)

	def homepage(self) -> dict:
		text = self._getPage(self.domain)
		s = BeautifulSoup(text, features = "lxml")
		tables = s.find_all("table")

		return {
			"news": [[x.a.get("href"), *x.text.split(": ")] for x in tables[0].find_all("td")], # Link	Date	Title
			# "dailyjak": "", # fucking retard quote broke the dailyjak
			"pph": [[x.a.get("href").split("/")[1], *(cInt(y.text) for y in x.find_all("td"))] for x in tables[1].find_all("tr")[1:]], # Link	Title	BoardDescription	PPH	Posters	PostCount
			"statistics": [float(x.text.split(": ")[1].replace(",", "").split(" ")[0]) for x in s.find_all("div", class_ = "box left")[1].find_all("li")] # Posts	Posters	ActiveContentGB
		}

	def __init__(
		self,
		domain: str,
		mcchallenge: str,
		emulation = Emulation.Firefox147,
		headers: dict = {}
	):
		self.domain = domain

		self.headers = HeaderMap()

		for k, v in headers.items():
			self.headers[k] = v

		jar = Jar()
		jar.add(Cookie(name = "_____mcchallenge", value = mcchallenge), DOMAIN)

		self.client = Client(
			emulation = emulation,
			headers = self.headers,
			cookie_jar = jar
		)
		self.phrases = [ # TODO make this shit more logical
			"big black cock",
			"big white cock",
			"bwc",
			"BWĆ",
			"bbc",
			"twp",
			"tiny white",
			"bnwo",
			"blacked",
			"clitty",
			"chastity",
			"caged",
			"plap",
			"sissygasm",
			"leaking",
			"gooning",
			"whiteboi",
			"her face when",
			"bussy"
		]

class Program:
	def sql(self, statement, values = []):
		if self.args.verbose: # print queries so we can see if we have fucked up the SQL
			stmt = statement.replace("%s", "{}")

			if values != []:
				stmt = stmt.format(*values)
			print(stmt)

		self.cursor.execute(statement, [*values])

		if not self.args.nocommit:
			self.connection.commit()
		return self.cursor.fetchall()

	def __init__(self):
		parser = argparse.ArgumentParser(description = "Gather data from soyjak.st / soyjakwiki.org and insert into sql database")
		parser.add_argument("--credentials", action = "store", type = str, default = "$SOYSCRAPERDBCREDS", help = "Env to load credentials from")
		parser.add_argument("-v", "--verbose", action = "store_true", dest = "verbose", help = "Print extra info (sql commands)")
		parser.add_argument("-n", "--nocommit", action = "store_true", dest = "nocommit", help = "No commit (dry-run)")
		self.args = parser.parse_args()

		logging.basicConfig(
			filename = os.path.join(os.path.dirname(__file__), "scraper.log"), # log at directory file located
			filemode = "a",
			format = "Time: `%(asctime)s` Line: %(lineno)d %(message)s",
			datefmt = "%d/%m/%Y %H:%M:%S",
			level = logging.ERROR
		)
		self.logger = logging.getLogger("scraper.log")

		try:
			with open(os.path.expanduser(os.path.expandvars(self.args.credentials))) as fp:
				credentials = json.load(fp)

			self.connection = mysql.connector.connect(
				host = credentials["host"],
				port = credentials["port"],
				user = credentials["username"],
				password = credentials["password"],
				database = credentials["database"],
				buffered = True
			)
			self.cursor = self.connection.cursor()

			self.scraper = Scraper(
				domain = DOMAIN,
				headers = {
					"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
					"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
					"Accept-Language": "en-US,en;q=0.9",
					"Referer": "https://soyjak.st/",
					"Connection": "keep-alive",
					"Upgrade-Insecure-Requests": "1",
					"Sec-Fetch-Dest": "document",
					"Sec-Fetch-Mode": "navigate",
					"Sec-Fetch-Site": "same-origin",
					"Sec-Fetch-User": "?1",
					"Priority": "u=0, i",
					"TE": "trailers"
				},
				mcchallenge = credentials["mcchallenge"]
			)

			# BEGIN
			try:
				homepage = self.scraper.homepage()
			except Exception as exception:
				self.logger.error(f"Got exception whilst scraping homepage: {exception}")
				exit()

			ts = round(time.time())

			for headline in homepage["news"]:
				try:
					self.sql("INSERT IGNORE INTO `news` (link, added, title, time) VALUES (%s, %s, %s, %s)", [*headline, ts])
				except Exception as exception:
					self.logger.error(f"Got exception whilst inserting headline data: `{exception}`")

			descriptions = []

			for board in homepage["pph"]:
				try:
					descriptions.append([board[0], board.pop(1), board.pop(1)])
					self.sql("INSERT INTO `pph` (board, pph, posters, count, time) VALUES (%s, %s, %s, %s, %s)", [*board, ts])
				except Exception as exception:
					self.logger.error(f"Got exception whilst inserting board data: `{exception}`")

			for description in descriptions: # save board descriptions when they change. insert if latest record is different from title / description
				try:
					r = self.sql("SELECT title, description FROM `descriptions` WHERE `board` = %s ORDER BY `descriptions`.`time` DESC LIMIT 1", [board := description[0]])
					insert = False

					if r == []: # ran before
						insert = True
					elif list(r[0]) != description[1:]:
						# print(list(r[0]) == description[1:])
						insert = True

					if insert:
						self.sql("INSERT INTO `descriptions` (board, title, description, time) VALUES (%s, %s, %s, %s)", [*description, ts])
				except Exception as exception:
					self.logger.error(f"Got exception whilst processing / inserting board description data: `{exception}`")

			try:
				self.sql("INSERT INTO `statistics` (posts, posters, content, time) VALUES (%s, %s, %s, %s)", [*homepage["statistics"], ts])
			except Exception as exception:
				self.logger.error(f"Got exception whilst inserting statistics data: `{exception}`")

			try:
				latestRtlFromServer = self.sql("SELECT `time` FROM `rtl` ORDER BY `rtl`.`time` DESC LIMIT 1")[0][0]

				for rtl in list(self.scraper.rtl()):
					if rtl[2] > latestRtlFromServer:
						# print(rtl[2], latestRtlFromServer)
						self.sql("INSERT INTO `rtl` (score, voters, time) VALUES (%s, %s, %s)", rtl)
			except Exception as exception:
				self.logger.error(f"Got exception whilst inserting rtl data: `{exception}`")

			try:
				jewCount = self.scraper.jewdar("soy") # TODO do multiple boards
				self.sql("INSERT INTO `jewdar` (count, time) VALUES (%s, %s)", [jewCount, ts])
			except Exception as exception:
				self.logger.error(f"Got exception whilst inserting jewdar data: `{exception}`")
			# END

			self.cursor.close()
			self.connection.close()

		except Exception as exception:
			self.logger.error(f"Undefined error: {exception}")

if __name__ == "__main__":
	Program()
