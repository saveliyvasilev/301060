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
import group

class DeterministicNode(object):
	"""
	Placeholder in the fixture. 
	This is used for modeling the knockout stage.
	"""
	def __init__(self, id, fn_team=None, fn1=None, fn2=None):
		"""
		Instantiate either with {fn} or {fn1, fn2}.
		fn is the leaf node (name of the team).
		fn1 and fn2 are the children nodes (DeterministicNode).
		"""
		if not (
			(fn_team is None and (fn1 is not None and fn2 is not None)) or
			(fn_team is not None and (fn1 is None and fn2 is None))
			):
			raise ValueError("Either a team name (fn) must be given or two child nodes (fn1 fn2) must be given.")

		self._fn1 = fn1
		self._fn2 = fn2
		self._winner = fn_team

		self._loser = None
		self.id = id
		self._match = None

	def _execute(self):
		if self._winner is not None:
			return
		team1 = self._fn1.winner()
		team2 = self._fn2.winner()
		if self._match is None:
			self._match = match.Match(team1, team2, id=self.id, knockout=True)
		else:
			if not self._match.knockout:
				raise Exception("A match that can be drawn was loaded into knockout phase. This is not acceptable.")
			if not ((self._match.team1 == team1 and self._match.team2 == team2) or 
				(self._match.team1 == team2 and self._match.team2 == team1)):
				raise Exception("The simulation arrived at a situation when " +
					"a loaded match isn't the played one. Check for previous matches for {}. ".format(self.id) +
					"The mismatch is as follows:\n" +
					"Match loaded = {}\nTeams reached by simulation: {} vs {}.".format(
						str(self._match), team1, team2))
		self._winner = self._match.winner()
		self._loser = self._match.loser()

	def winner(self):
		self._execute()
		return self._winner

	def loser(self):
		self._execute()
		return self._loser

	def match(self):
		self._execute()
		if self._match is None:
			raise RuntimeWarning("There is no match in this DeterministicNode.")
		return self._match

	def retrieve_nodes(self, ids):
		ns = []
		if self._fn1 is not None:
			ns += self._fn1.retrieve_nodes(ids)
		if self._fn2 is not None:
			ns += self._fn2.retrieve_nodes(ids)
		if self.id in ids:
			ns.append(self)
		return ns

	def set_matches(self, matches):
		"""
		Used for defining encounters in the tree according to matches passed as parameters.
		The ids are used to identify the matches. 
		"""
		if self._fn1 is not None:
			self._fn1.set_matches(matches)
		if self._fn2 is not None:
			self._fn2.set_matches(matches)
		if self.id in matches:
			self._match = matches[self.id]
		return

	def __str__(self):
		self._execute()
		if self._fn1:
			left = str(self._fn1)
			right = str(self._fn2)
			return ("({1}) {0} ({2})").format(self.id, left, right)
		else: 
			return self.id

	def __iter__(self):
		if self._fn1 is not None:
			for n in self._fn1:
				yield n
		if self._fn2 is not None:
			for n in self._fn2:
				yield n
		# Skip the leaves
		if self._fn1 is None: 	
			return
		if self._fn2 is None:
			return
		yield self