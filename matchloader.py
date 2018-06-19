#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 by Instituto de Cálculo, http://www.ic.fcen.uba.ar/

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Coded by Saveliy Vasiliev for project 301060 (https://301060.exactas.uba.ar/)

import config
import match
import deterministicnode as dnode
import group
import estimations as est
import fixture_data as fd
import pprint
import hashlib
import logging
import sys
import simulator as sim
from pymongo import MongoClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(filename)s(%(lineno)d):%(funcName)s:%(message)s")
stream_formatter = logging.Formatter("%(levelname)s:%(message)s")

file_handler = logging.FileHandler('log/matchloader.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(config.file_logging_level)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(config.stream_logging_level)
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class MatchLoader(object):
	"""
	This class is used for interacting with the mongo db, for
	storing and retrieving matches from the database.
	"""
	def __init__(self):
		pass

	@classmethod
	def store_group_match(cls, match):
		try:
		# Stores match in mongo if there is no another match with the same hash.
			mdb_client = MongoClient('mongodb://localhost:27017/')
			collection = mdb_client.worldcup18.group_matches
			if collection.find_one({"hash": hash(match)}) is None:
				collection.insert_one(cls._match_to_dictionary(match))
				logger.info("Added match [{}] to group matches (MongoDB).".format(str(match)))
			else:
				logger.debug("Match [{}] already in DB.".format(str(match)))
			return
		except Exception as e:
		 	logger.exception("Error storing match [{}] in database.".format(str(match)))
		 	sys.exit()

	@classmethod
	def store_knockout_match(cls, match, slot):
		try:
			mdb_client = MongoClient('mongodb://localhost:27017/')
			collection = mdb_client.worldcup18.knockout_matches
			if not match.knockout:
				raise Exception("The knockout match must be instantiated with knockout=True.")
			if collection.find_one({"hash": hash(match), "slot": slot}) is None:
				slot_match = cls._match_to_dictionary(match)
				slot_match["slot"] = slot
				collection.insert_one(slot_match)
				logger.info("Added match [{}] to knockout matches (MongoDB).".format(str(match)))
			else:
				logger.debug("Match [{}] already in DB.".format(str(match)))
			return
		except Exception as e:
		 	logger.exception("Error storing a match.")
		 	sys.exit()


	@classmethod
	def load_knockout_matches(cls):
		try:
			mdb_client = MongoClient('mongodb://localhost:27017/')
			db = mdb_client.worldcup18
			collection = db.knockout_matches
			qms = collection.find()
			ms = {q["slot"]:
						match.Match(
						team1=q["team1"], 
						team2=q["team2"], 
						goals1=q["goals1"],
						goals2=q["goals2"], 
						knockout=q["knockout"],
						winner=q["winner"] if "winner" in q else None,
						id=q["id"] if "id" in q else None)
					for q in qms}
			mdb_client.close()
			return ms
		except Exception as e:
		 	logger.exception("Error loading knockout matches.")
		 	sys.exit()

	@classmethod
	def load_group_matches(cls):
		try:
			mdb_client = MongoClient('mongodb://localhost:27017/')
			db = mdb_client.worldcup18
			collection = db.group_matches
			qms = collection.find()
			ms = [match.Match(
					team1=q["team1"], 
					team2=q["team2"], 
					goals1=q["goals1"],
					goals2=q["goals2"], 
					knockout=q["knockout"],
					winner=q["winner"] if "winner" in q else None,
					id=q["id"] if "id" in q else None)
					for q in qms]
			mdb_client.close()
			return ms
		except Exception as e:
		 	logger.exception("Error loading group matches.")
		 	sys.exit()


	@classmethod
	def _match_to_dictionary(cls, match):
		return {
			"hash": hash(match),
			"team1": match.team1,
			"team2": match.team2,
			"goals1": match.score()[match.team1],
			"goals2": match.score()[match.team2],
			"knockout": match.knockout,
			"id": match.id,
			"winner": match.winner()
		}


	def __str__(self):
		return "CashableSimulator <Hash: {}>".format(self._hash)


def store_worldcup():
	# A
	MatchLoader.store_group_match(match.Match("RUS", "KSA", 5, 0))
	MatchLoader.store_group_match(match.Match("EGY", "URU", 0, 1))
	# MatchLoader.store_group_match(match.Match("RUS", "EGY", 0, 0))
	# MatchLoader.store_group_match(match.Match("URU", "KSA", 0, 0))
	# MatchLoader.store_group_match(match.Match("URU", "RUS", 2, 0))
	# MatchLoader.store_group_match(match.Match("KSA", "EGY", 0, 0))
	# # B
	MatchLoader.store_group_match(match.Match("ESP", "POR", 3, 3))
	MatchLoader.store_group_match(match.Match("MAR", "IRN", 0, 1))
	# MatchLoader.store_group_match(match.Match("MAR", "POR", 0, 1))
	# MatchLoader.store_group_match(match.Match("IRN", "ESP", 0, 0))
	# MatchLoader.store_group_match(match.Match("IRN", "POR", 0, 0))
	# MatchLoader.store_group_match(match.Match("MAR", "ESP", 0, 0))
	# # C
	MatchLoader.store_group_match(match.Match("AUS", "FRA", 1, 2))
	MatchLoader.store_group_match(match.Match("PER", "DEN", 0, 1))
	# MatchLoader.store_group_match(match.Match("PER", "FRA", 0, 2))
	# MatchLoader.store_group_match(match.Match("AUS", "DEN", 0, 0))
	# MatchLoader.store_group_match(match.Match("FRA", "DEN", 0, 0))
	# MatchLoader.store_group_match(match.Match("AUS", "PER", 0, 1))
	# # D 
	MatchLoader.store_group_match(match.Match("ICE", "ARG", 1, 1))
	MatchLoader.store_group_match(match.Match("NGA", "CRO", 0, 2))
	# MatchLoader.store_group_match(match.Match("CRO", "ARG", 0, 2))
	# MatchLoader.store_group_match(match.Match("ICE", "NGA", 0, 0))
	# MatchLoader.store_group_match(match.Match("NGA", "ARG", 0, 0))
	# MatchLoader.store_group_match(match.Match("ICE", "CRO", 0, 0))
	# # E
	MatchLoader.store_group_match(match.Match("SWI", "BRA", 1, 1))
	MatchLoader.store_group_match(match.Match("CRC", "SRB", 0, 1))
	# MatchLoader.store_group_match(match.Match("BRA", "CRC", 0, 0))
	# MatchLoader.store_group_match(match.Match("SWI", "SRB", 1, 0))
	# MatchLoader.store_group_match(match.Match("BRA", "SRB", 0, 0))
	# MatchLoader.store_group_match(match.Match("SWI", "CRC", 0, 0))
	# # F
	MatchLoader.store_group_match(match.Match("MEX", "GER", 1, 0))
	MatchLoader.store_group_match(match.Match("KOR", "SWE", 0, 1))
	# MatchLoader.store_group_match(match.Match("SWE", "GER", 0, 0))
	# MatchLoader.store_group_match(match.Match("KOR", "MEX", 0, 1))
	# MatchLoader.store_group_match(match.Match("KOR", "GER", 0, 0))
	# MatchLoader.store_group_match(match.Match("SWE", "MEX", 0, 0))
	# # G
	MatchLoader.store_group_match(match.Match("PAN", "BEL", 0, 3))
	MatchLoader.store_group_match(match.Match("ENG", "TUN", 2, 1))
	# MatchLoader.store_group_match(match.Match("TUN", "BEL", 0, 0))
	# MatchLoader.store_group_match(match.Match("ENG", "PAN", 0, 0))
	# MatchLoader.store_group_match(match.Match("ENG", "BEL", 2, 0))
	# MatchLoader.store_group_match(match.Match("PAN", "TUN", 0, 0))
	# # H
	# MatchLoader.store_group_match(match.Match("POL", "SEN", 1, 0))
	# MatchLoader.store_group_match(match.Match("COL", "JPN", 0, 0))
	# MatchLoader.store_group_match(match.Match("COL", "POL", 2, 0))
	# MatchLoader.store_group_match(match.Match("JPN", "SEN", 0, 0))
	# MatchLoader.store_group_match(match.Match("JPN", "POL", 0, 0))
	# MatchLoader.store_group_match(match.Match("COL", "SEN", 0, 0))



	# # # Round2 knockout matches
	# MatchLoader.store_knockout_match(match.Match("URU", "POR", 1, 2, knockout=True, id="S1"), slot="S1")
	# MatchLoader.store_knockout_match(match.Match("FRA", "CRO", 0, 2, knockout=True, id="S2"), slot="S2")
	# MatchLoader.store_knockout_match(match.Match("ESP", "RUS", 1, 3, knockout=True, id="S3"), slot="S3")
	# MatchLoader.store_knockout_match(match.Match("ARG", "PER", 3, 2, knockout=True, id="S4"), slot="S4")
	# MatchLoader.store_knockout_match(match.Match("BRA", "MEX", 1, 0, knockout=True, id="S5"), slot="S5")
	# MatchLoader.store_knockout_match(match.Match("ENG", "POL", 2, 0, knockout=True, id="S6"), slot="S6")
	# MatchLoader.store_knockout_match(match.Match("SWI", "GER", 1, 2, knockout=True, id="S7"), slot="S7")
	# MatchLoader.store_knockout_match(match.Match("COL", "BEL", 3, 0, knockout=True, id="S8"), slot="S8")


	# # # QF knockout matches
	# MatchLoader.store_knockout_match(match.Match("POR", "CRO", 1, 2, knockout=True, id="Q1"), slot="Q1")
	# MatchLoader.store_knockout_match(match.Match("BRA", "ENG", 2, 2, knockout=True, winner="BRA", id="Q2"), slot="Q2")
	# MatchLoader.store_knockout_match(match.Match("RUS", "ARG", 1, 3, knockout=True, id="Q3"), slot="Q3")
	# MatchLoader.store_knockout_match(match.Match("GER", "COL", 3, 2, knockout=True, id="Q4"), slot="Q4")

	# # # SF knockout matches
	# MatchLoader.store_knockout_match(match.Match("CRO", "BRA", 1, 0, knockout=True, id="SF1"), slot="SF1")
	# MatchLoader.store_knockout_match(match.Match("GER", "ARG", 2, 1, knockout=True, id="SF2"), slot="SF2")


	# # # Final knockout matches
	# MatchLoader.store_knockout_match(match.Match("BRA", "ARG", 1, 2, knockout=True, id="ThirdPlace"), slot="ThirdPlace")
	# MatchLoader.store_knockout_match(match.Match("CRO", "GER", 1, 0, knockout=True, id="Final"), slot="Final")


if __name__ == '__main__':
	store_worldcup()
