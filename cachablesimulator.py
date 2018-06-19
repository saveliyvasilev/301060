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

import match
import deterministicnode as dnode
import group
import estimations as est
import fixture_data as fd
import pprint
import hashlib
import simulator as sim
from pymongo import MongoClient
import sys
import config
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(filename)s(%(lineno)d):%(funcName)s:%(message)s")
stream_formatter = logging.Formatter("%(levelname)s:%(message)s")

file_handler = logging.FileHandler('log/cachablesimulator.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(config.file_logging_level)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(config.stream_logging_level)
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class CachableSimulator(object):
	"""
	This class searches the mongo database to see whether the passed known matches
	were already simulated and if there is a simulation it uses that data. Otherwise,
	it runs a simulator with these parameters, then saves its output to the db and
	uses that data as before.
	"""
	def __init__(self, group_matches=[], knockout_matches={}):
		"""
		group_matches: the set of matches already played. The rest will be generated 
			based on the data in fixture_data.py
		knockout_matches: a dictionary {slot_label:match}.
		"""

		round_leaves = ["A1","A2","B1","B2","C1","C2","D1","D2","E1","E2","F1","F2","G1","G2","H1","H2"]
		round2 = ["S1","S2","S3","S4","S5","S6","S7","S8"]
		round_qf = ["Q1","Q2","Q3","Q4"]
		round_sf = ["SF1","SF2"]
		round_f = ["Final"]
		ko_node_labels = round_leaves + round2 + round_qf + round_sf + round_f

		group_hash = self._hash_match_list(group_matches)
		ko_hash = self._hash_match_dicc(knockout_matches)
		iterations_hash = self._iterations_hash(config.iterations)
		self._hash = (group_hash + ko_hash + iterations_hash) % 100000000000000000

		logger.debug("Group hash:     {}".format(group_hash))
		logger.debug("Knockout hash:  {}".format(ko_hash))
		logger.debug("Simulation hash:{}".format(self._hash))
		simdata = self._get_simulation_from_db()
		if simdata:
			logger.debug("Simulation exists at DB! Populating data.")
			self._populate_data_from_query_result(simdata)
		else:
			logger.info("Simulation is not pre-computed. Will simulate now, this will take a while.")
			try:
				simulator = sim.Simulator(group_matches, knockout_matches, iterations=config.iterations)
				logger.info("Simulation completed. Saving into DB.")
				self._populate_data_from_simulator(simulator)
				self._save()
			except Exception as e:
				logger.exception("Could not run the simulation.")
				sys.exit()


	def _hash_match_list(self, ms):
		return sum([hash(m) for m in ms])

	def _iterations_hash(self, iterations):
		return int(hashlib.md5(iterations.to_bytes(4, 'big')).hexdigest(), 16) & 0xffffffffffffffff

	def _hash_match_dicc(self, d):
		return sum([(
			int(hashlib.md5((slot + str(hash(match))).encode()).hexdigest(), 16) 
			& 0xffffffffffffffff)
			for slot, match in d.items()
			])


	def _get_simulation_from_db(self):
		try:
			mdb_client = MongoClient('mongodb://localhost:27017/')
			db = mdb_client.worldcup18
			collection = db.simulations
			simdata = collection.find_one({"hash" : self._hash})
			mdb_client.close()
			return simdata
		except Exception as e:
			logger.exception("Could not obtain simulation info from database.")
			sys.exit()


	def _populate_data_from_simulator(self, sim):
		self._probs_reaching_node = sim.probs_reaching_node()
		self._probs_pair_playing_at_node = sim.probs_pair_playing_at_node()
		self._probs_group_position = sim.probs_group_position()
		self._probs_champion = sim.probs_champion()
		self._probs_second = sim.probs_second()
		self._probs_third = sim.probs_third()
		return


	def _populate_data_from_query_result(self, qresult):
		self._probs_reaching_node = qresult["probs_reaching_node"]
		self._probs_pair_playing_at_node = qresult["probs_pair_playing_at_node"]
		self._probs_group_position = qresult["probs_group_position"]
		self._probs_champion = qresult["probs_champion"]
		self._probs_second = qresult["probs_second"]
		self._probs_third = qresult["probs_third"]
		return


	def _save(self):
		try:
			mdb_client = MongoClient('mongodb://localhost:27017/')
			db = mdb_client.worldcup18
			collection = db.simulations
			collection.insert_one({
				"hash" : self._hash, 
				"probs_reaching_node": self.probs_reaching_node(),
				"probs_pair_playing_at_node": self.probs_pair_playing_at_node(),
				"probs_group_position": self.probs_group_position(),
				"probs_champion": self.probs_champion(),
				"probs_second": self.probs_second(),
				"probs_third": self.probs_third()
				})
			mdb_client.close()
		except Exception as e:
			logger.exception("Could not save simulation to database.")
			sys.exit()

	def probs_reaching_node(self):
		return self._probs_reaching_node

	def probs_pair_playing_at_node(self):
		return self._probs_pair_playing_at_node

	def probs_group_position(self):
		return self._probs_group_position

	def probs_champion(self):
		return self._probs_champion

	def probs_second(self):
		return self._probs_second

	def probs_third(self):
		return self._probs_third

	def __str__(self):
		return "CashableSimulator <Hash: {}>".format(self._hash)


if __name__ == '__main__':
	ma1 = match.Match("KSA", "RUS", 1, 2)
	ma2 = match.Match("EGY", "URU", 2, 0)
	ma3 = match.Match("URU", "RUS", 0, 1)
	ma4 = match.Match("KSA", "URU", 10, 0)
	ma5 = match.Match("RUS", "EGY", 1, 0)
	ma6 = match.Match("EGY", "KSA", 1, 0)
	csim = CachableSimulator([ma1, ma2, ma3, ma4, ma5, ma6])
	pprint.pprint(csim.probs_group_position()["A"])
	print(csim)
