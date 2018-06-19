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
import config
import sys

class Simulator(object):
	"""
	Simulator that supports pre-defined inputs. Runs and stores statistics for each team.
	"""
	def __init__(self, group_matches, knockout_matches, iterations, instance_callbacks=[]):
		"""
		group_matches: the set of matches already played. The rest will be generated 
			based on the data in fixture_data.py
		knockout_matches: a dictionary {slot_label:match}, see implementation of _run_instance for the ids used.
			Yeah, I know, it's not that accurate, you're welcome to tidy this up :)
		"""
		ko_node_labels = ["A1","A2","B1","B2","C1","C2","D1","D2","E1","E2","F1","F2","G1","G2","H1","H2",
						  "S1","S2","S3","S4","S5","S6","S7","S8","Q1","Q2","Q3","Q4","SF1","SF2","Final"]
		self._group_matches = group_matches
		self._known_group_pairs = []
		self._build_known_group_pairs()
		self._knockout_matches = knockout_matches
		self._team_in_node_count = dict(zip(ko_node_labels, 
			[{} for _ in range(len(ko_node_labels))]))
		self._teams_in_node_count = dict(zip(ko_node_labels, 
			[{} for _ in range(len(ko_node_labels))]))
		self._team_in_group_position = dict(zip(fd.groups.keys(), 
			[{} for _ in range(len(fd.groups.keys()))]))
		teams = [team for group_teams in fd.groups.values() for team in group_teams]
		self._champion_count = dict(zip(teams, [0] * len(teams)))
		self._second_place_count = dict(zip(teams, [0] * len(teams)))
		self._third_place_count = dict(zip(teams, [0] * len(teams)))
		self._initialize_group_counters()
		self._iterations = iterations
		self._instance_callbacks = instance_callbacks
		self._run()


	def _run(self):
		update_step = 100
		for i in range(self._iterations):
			if i % update_step == 0:
				self._update_progress(i)
			self._run_instance()
		self._update_progress(self._iterations)


	def _update_progress(self, i):
		length = 40
		progress = i / self._iterations
		block = int(round(length*progress))
		msg = "\rSimulation: [{0}] {1:.2f}% ({2} / {3})".format(
			"#"*block + "-"*(length-block), 
			round(progress*100, 4),
			i,
			self._iterations)
		if progress >= 1: 
			msg += " DONE\r\n"
		sys.stdout.write(msg)
		sys.stdout.flush()

	def _inc_team_in_node_count(self, nodeid, team):
		if team not in self._team_in_node_count[nodeid]:
			self._team_in_node_count[nodeid][team] = 0
		self._team_in_node_count[nodeid][team] += 1

	def _inc_teams_in_node_count(self, nodeid, team1, team2):
		if team1 not in self._teams_in_node_count[nodeid]:
			self._teams_in_node_count[nodeid][team1] = {}
		if team2 not in self._teams_in_node_count[nodeid][team1]:
			self._teams_in_node_count[nodeid][team1][team2] = 0
		self._teams_in_node_count[nodeid][team1][team2] += 1
		
		if team2 not in self._teams_in_node_count[nodeid]:
			self._teams_in_node_count[nodeid][team2] = {}
		if team1 not in self._teams_in_node_count[nodeid][team2]:
			self._teams_in_node_count[nodeid][team2][team1] = 0
		self._teams_in_node_count[nodeid][team2][team1] += 1


	def _update_counters(self, knockout_phase, groups, third_place=None):
		if knockout_phase.id != "Final":
			raise ValueError("knockout_phase has id != 'Final'.") 

		self._champion_count[knockout_phase.winner()] += 1
		self._second_place_count[knockout_phase.loser()] += 1
		if third_place:
			self._third_place_count[third_place.winner()] += 1

		for node in knockout_phase:
			self._inc_team_in_node_count(node.id, node.winner())
			self._inc_team_in_node_count(node.id, node.loser())
			self._inc_teams_in_node_count(node.id, node.winner(), node.loser())
		for gname, group in groups.items():
			self._team_in_group_position[gname][group.first()]["1"] += 1
			self._team_in_group_position[gname][group.second()]["2"] += 1
			self._team_in_group_position[gname][group.third()]["3"] += 1
			self._team_in_group_position[gname][group.fourth()]["4"] += 1

	def _build_instance_group_matches(self, group_name):
		ms = []
		for fixture_match in fd.group_pairs[group_name]:
			if fixture_match in self._known_group_pairs:
				known_match = next(km for km in self._group_matches if {km.team1, km.team2} == fixture_match)
				ms.append(match.Match.from_match(known_match))
			else:
				it = iter(fixture_match)
				ms.append(match.Match(next(it), next(it)))
		return ms

	def _build_instance_groups(self):
		gs = {}
		for g in fd.groups:
			gs[g] = group.Group(self._build_instance_group_matches(g), id = g)
		return gs


	def _build_known_group_pairs(self):
		for m in self._group_matches:
			self._known_group_pairs.append({m.team1, m.team2})


	def _initialize_group_counters(self):
		# The indexing is group,team,position.
		for gname, teams in fd.groups.items():
			for team in teams:
				self._team_in_group_position[gname][team] = dict(zip(["1","2","3","4"], [0,0,0,0]))


	def _run_instance(self):
		groups = self._build_instance_groups()

		a1 = dnode.DeterministicNode("A1", fn_team=groups["A"].first())
		a2 = dnode.DeterministicNode("A2", fn_team=groups["A"].second())
		b1 = dnode.DeterministicNode("B1", fn_team=groups["B"].first())
		b2 = dnode.DeterministicNode("B2", fn_team=groups["B"].second())
		c1 = dnode.DeterministicNode("C1", fn_team=groups["C"].first())
		c2 = dnode.DeterministicNode("C2", fn_team=groups["C"].second())
		d1 = dnode.DeterministicNode("D1", fn_team=groups["D"].first())
		d2 = dnode.DeterministicNode("D2", fn_team=groups["D"].second())
		e1 = dnode.DeterministicNode("E1", fn_team=groups["E"].first())
		e2 = dnode.DeterministicNode("E2", fn_team=groups["E"].second())
		f1 = dnode.DeterministicNode("F1", fn_team=groups["F"].first())
		f2 = dnode.DeterministicNode("F2", fn_team=groups["F"].second())
		g1 = dnode.DeterministicNode("G1", fn_team=groups["G"].first())
		g2 = dnode.DeterministicNode("G2", fn_team=groups["G"].second())
		h1 = dnode.DeterministicNode("H1", fn_team=groups["H"].first())
		h2 = dnode.DeterministicNode("H2", fn_team=groups["H"].second())

		s1 = dnode.DeterministicNode("S1", fn1=a1, fn2=b2)
		s2 = dnode.DeterministicNode("S2", fn1=c1, fn2=d2)
		s3 = dnode.DeterministicNode("S3", fn1=b1, fn2=a2)
		s4 = dnode.DeterministicNode("S4", fn1=d1, fn2=c2)
		s5 = dnode.DeterministicNode("S5", fn1=e1, fn2=f2)
		s6 = dnode.DeterministicNode("S6", fn1=g1, fn2=h2)
		s7 = dnode.DeterministicNode("S7", fn1=f1, fn2=e2)
		s8 = dnode.DeterministicNode("S8", fn1=h1, fn2=g2)

		q1 = dnode.DeterministicNode("Q1", fn1=s1, fn2=s2)
		q2 = dnode.DeterministicNode("Q2", fn1=s5, fn2=s6)
		q3 = dnode.DeterministicNode("Q3", fn1=s3, fn2=s4)
		q4 = dnode.DeterministicNode("Q4", fn1=s7, fn2=s8)

		sf1 = dnode.DeterministicNode("SF1", fn1=q1, fn2=q2)
		sf2 = dnode.DeterministicNode("SF2", fn1=q3, fn2=q4)

		
		final = dnode.DeterministicNode("Final", fn1=sf1, fn2=sf2)
		
		final.set_matches(self._knockout_matches)

		third_place_candidate_1 = dnode.DeterministicNode("ThirdPlace1", fn_team=sf1.loser())
		third_place_candidate_2 = dnode.DeterministicNode("ThirdPlace2", fn_team=sf2.loser())
		third_place = dnode.DeterministicNode("ThirdPlace", fn1=third_place_candidate_1, fn2=third_place_candidate_2)
		third_place.set_matches(self._knockout_matches)

		self._update_counters(final, groups, third_place=third_place)
		for callback in self._instance_callbacks:
			callback(final, groups, third_place=third_place)


	def probs_reaching_node(self):
		# node x team
		probs = {}
		for nodeid in self._team_in_node_count:
			if self._team_in_node_count[nodeid]:
				probs[nodeid] = {}
			for team in self._team_in_node_count[nodeid]:
				probs[nodeid][team] = self._team_in_node_count[nodeid][team] / self._iterations
		return probs


	def probs_pair_playing_at_node(self):
		# node x team1 x team2: P(team1 faces team2 given that team1 reached node1)
		probs = {}

		for nodeid in self._teams_in_node_count:
			if self._teams_in_node_count[nodeid]:
				probs[nodeid] = {}
			for team1 in self._teams_in_node_count[nodeid]:
				probs[nodeid][team1] = {}
				for team2 in self._teams_in_node_count[nodeid][team1]:
					probs[nodeid][team1][team2] = self._teams_in_node_count[nodeid][team1][team2] / self._team_in_node_count[nodeid][team1]
		return probs

	def probs_group_position(self):
		# group x team x position; estimated as #(team in pos) / #(iterations)
		probs = {}
		for gname in self._team_in_group_position:
			probs[gname] = {}
			for team in self._team_in_group_position[gname]:
				probs[gname][team] = {}
				for pos in self._team_in_group_position[gname][team]:
					probs[gname][team][pos] = self._team_in_group_position[gname][team][pos] / self._iterations
		return probs

	def probs_champion(self):
		return {team: self._champion_count[team] / self._iterations for team in self._champion_count}

	def probs_second(self):
		return {team: self._second_place_count[team] / self._iterations for team in self._second_place_count}

	def probs_third(self):
		return {team: self._third_place_count[team] / self._iterations for team in self._third_place_count}

	def __str__(self):
		return "Simulator: {0}\nKnown group matches: {1}\nKnown knockout matches:{2}".format(
			self.__repr__(), 
			self._known_group_pairs,
			pprint.pformat(self._knockout_matches)
		)


if __name__ == '__main__':
	ma1 = match.Match("RUS", "KSA", 1, 0)
	ma2 = match.Match("EGY", "URU", 2, 0)
	def dummy_callback(final_node, groups, third_place):
		print("The champion is {}".format(final_node.winner()))
	sim = Simulator([], {}, config.iterations, instance_callbacks=[dummy_callback])
	pppan = sim.probs_pair_playing_at_node()
	pchamp = sim.probs_champion()
	psecond = sim.probs_second()
	pthird = sim.probs_third()
	
	print("Prob_Final(Arg vs Rus | Arg reached Final) = {0}".format(pppan["Final"]["ARG"]["RUS"]))
	print("Prob_Final(Arg vs Rus | Rus reached Final) = {0}".format(pppan["Final"]["RUS"]["ARG"]))
	print("Prob_Final(Bra vs Ale | Bra reached Final) = {0}".format(pppan["Final"]["BRA"]["GER"]))
	print("Prob_Final(Bra vs Ale | Ale reached Final) = {0}".format(pppan["Final"]["GER"]["BRA"]))
	print("Prob_Q4   (Ale vs Col | Ale reached Q4)    = {0}".format(pppan["Q4"]["GER"]["COL"]))
	print("Prob_Q4   (Ale vs Col | Col reached Q4)    = {0}".format(pppan["Q4"]["COL"]["GER"]))
	print("Prob_champion(Ale)                         = {0}".format(pchamp["GER"]))
	print("Prob_champion(Arg)                         = {0}".format(pchamp["ARG"]))
	print("Prob_champion(Col)                         = {0}".format(pchamp["COL"]))
	print("Prob_champion(Rus)                         = {0}".format(pchamp["RUS"]))
	print("Prob_second(Arg)                           = {0}".format(psecond["ARG"]))
	print("Prob_third(Arg)                            = {0}".format(pthird["ARG"]))