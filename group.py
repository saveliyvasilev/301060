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

import pprint
import random
import match 

class Group(object):
	"""
    Attributes:
        id: Some way of identifying this group, not required.
        matches: a set of matches within the group
    """
	def __init__(self, matches, id=None):
		self.id = id
		self._matches = matches
		self._teams = set([m.team1 for m in self._matches] 
						+ [m.team2 for m in self._matches])
		self._points = self._compute_points()
		self._goal_diffs = self._compute_goal_diffs()
		self._goals = self._compute_goals()
		self._result = None
		
	def _compute_points(self):
		points = dict(zip(self._teams, [0]*len(self._teams)))
		for m in self._matches:
			if m.winner() == m.team1:
				points[m.team1] += 3
			elif m.winner() == m.team2:
				points[m.team2] += 3
			else:
				points[m.team1] += 1
				points[m.team2] += 1
		return points

	def _compute_goal_diffs(self):
		goal_diffs = dict(zip(self._teams, [0]*len(self._teams)))
		for m in self._matches:
			r = m.score()
			goal_diffs[m.team1] += r[m.team1] - r[m.team2]
			goal_diffs[m.team2] += r[m.team2] - r[m.team1]
		return goal_diffs

	def _compute_goals(self):
		goals = dict(zip(self._teams, [0]*len(self._teams)))
		for m in self._matches:
			r = m.score()
			goals[m.team1] += r[m.team1]
			goals[m.team2] += r[m.team2]
		return goals

	def result(self):
		if self._result is None:
			self._result = sorted(self._teams, key=self._group_sort_key, reverse=True)
		return self._result

	def first(self):
		return self.result()[0]

	def second(self):
		return self.result()[1]

	def third(self):
		return self.result()[2]

	def fourth(self):
		return self.result()[3]

	def _group_sort_key(self, team):
		# The random.random is not the most accurate way of sorting teams in case of draw. Can be improved.
		return (self._points[team], self._goal_diffs[team], self._goals[team], random.random())

	def __str__(self):
		s = "Group {0}:\n{1:<20} {2:^6} {3:^6} {4:^6}".format(self.id, "Team", "Pts", "Diff", "Goals")
		for team in self.result():
			s += "\n{0:<20} {1:^6} {2:^6} {3:^6}".format(team, self._points[team], self._goal_diffs[team], self._goals[team])
		return s
		


if __name__ == "__main__":
	for _ in range(1000):
		m1 = match.Match("RUS", "KSA", 0, 0)
		m2 = match.Match("EGY", "URU", 0, 0)
		m3 = match.Match("RUS", "EGY", 3, 1)
		m4 = match.Match("URU", "KSA", 1, 3)
		m5 = match.Match("URU", "RUS", 2, 4)
		m6 = match.Match("KSA", "EGY", 4, 1)
		g = Group([m1, m2, m3, m4, m5, m6], id="A")
		g.result()
	print(g)
	print(g.result()) # Should be KSA, RUS, URU, EGY
