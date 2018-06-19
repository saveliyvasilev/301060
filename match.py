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

import estimations as est
import random
import pprint
import hashlib

class Match(object):
	"""
    Attributes:
        id: Some way of identifying this, not required.
        teams: Two strings representing teams
        knockout: True if the match cannot be a draw. False otherwise.
        goals: Two integers that represent the result of the game
        	   (This is used to pre-set some result)
    """
	def __init__(self, team1, team2, goals1=None, goals2=None, winner=None, knockout=False, id=None):
		if goals1 is not None and goals2 is None:
			raise ValueError("If goals1 is set, so must be goals2")
		if goals2 is not None and goals1 is None:
			raise ValueError("If goals2 is set, so must be goals1")
		if knockout and goals2 is not None and goals2 == goals1 and winner is None:
			raise ValueError("Can't initialize a knockout match which is a DRAW: " +
				"either a winner must be specified, or the goals differ.")
		if knockout and goals2 is not None and goals2 == goals1 and winner not in [team1, team2]:
			raise ValueError("Invalid winner {0}. Must be some of [{1}, {2}]".format(winner, team1, team2))
		self.id = id
		self.team1 = team1
		self.team2 = team2
		self._winner = None
		self._loser = None
		self.knockout = knockout
		if goals1 is not None:
			self._score = {team1: goals1, team2: goals2}
			if goals1 == goals2:
				self._winner = winner
				self._loser = self.team2 if self.team2 != self._winner else self.team1
			else:
				self._define_winner_and_loser()
		else:
			self._score = None

	@classmethod
	def from_match(cls, m):
		return	cls(team1 = m.team1, 
			team2 = m.team2, 
			goals1 = m._score[m.team1] if m._score is not None else None,
			goals2 = m._score[m.team2] if m._score is not None else None,
			winner = m._winner,
			knockout = m.knockout,
			id = m.id)
		

	def __str__(self):
		s = "{0}({1} vs. {2}) [hash={3}]".format(self.id+' ' if self.id is not None else '', self.team1, self.team2, self.__hash__())
		if self._score is not None:
			if self._score[self.team1] == self._score[self.team2]:
				s += " DRAW {0}-{1}".format(self._score[self.team1], self._score[self.team2])
				if self.knockout:
					s += " ({0} won by penalties)".format(self.winner())
				return s
			elif self._score[self.team1] > self._score[self.team2]:
				return s + " {0} WON {1}-{2}".format(self.team1, self._score[self.team1], self._score[self.team2])
			else:
				return s + " {0} WON {1}-{2}".format(self.team2, self._score[self.team2], self._score[self.team1])
		return s + " PENDING"


	def __hash__(self):
		s_ko = "KO" if self.knockout else "NOKO"
		if self.knockout:
			s_ko += str(self.winner())
		s_team1 = self.team1 + str(self._score[self.team1])
		s_team2 = self.team2+ str(self._score[self.team2])

		ko_hash = hashlib.md5(s_ko.encode())
		id_hash = hashlib.md5(self.id.encode()) if self.id else None
		team1_hash = hashlib.md5(s_team1.encode())
		team2_hash = hashlib.md5(s_team2.encode())

		ko_hash_int = int(ko_hash.hexdigest(), 16)
		id_hash_int = int(id_hash.hexdigest(), 16) if id_hash else 0
		team1_hash_int = int(team1_hash.hexdigest(), 16)
		team2_hash_int = int(team2_hash.hexdigest(), 16)

		hash_truncated = (ko_hash_int + team1_hash_int + team2_hash_int + id_hash_int) & 0xffffffffffffffff
		return hash_truncated


	def _play(self):
		if self._score is not None:
			raise RuntimeWarning("The match {0} vs. {1} is already played.".format(self.team1, self.team2))
		
		self._score = est.random_score(self.team1, self.team2)
		self._define_winner_and_loser()

	def _define_winner_and_loser(self):
		if self._score[self.team1] > self._score[self.team2]:
			self._winner = self.team1
			self._loser = self.team2
		elif self._score[self.team1] < self._score[self.team2]:
			self._winner = self.team2
			self._loser = self.team1
		if self.knockout and self._score[self.team1] == self._score[self.team2]:
			# penalties simply add one goal to some team
			self._winner = random.choice([self.team1, self.team2])
			self._loser = self.team2 if self.team2 != self._winner else self.team1


	def score(self):
		""" 
		Returns a dictionary holding the score DURING the match. If it was a knockout match
		one must ask for winner() or loser()
		"""
		if self._score is None:
			self._play()
		return self._score

	def winner(self):
		if self._score is None:
			self._play()
		return self._winner

	def loser(self):
		if self._score is None:
			self._play()
		return self._loser

	def is_between(team1, team2):
		if self.team1 == team1 and self.team2 == team2:
			return True
		elif self.team1 == team2 and self.team2 == team1:
			return True
		return False


if __name__ == "__main__":
	m = Match("RUS", "KSA", knockout=True, goals1=1, goals2=1, winner="RUS", id="TEST_1")
	print(m)
	print("hash: ", hash(m))


	m = Match("KSA", "RUS", knockout=True, goals1=1, goals2=1, winner="RUS", id="TEST_1")
	print(m)
	print("hash: ", hash(m))

	print("Hashes should be equal.")

