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

group_pairs_time_ordered = [
	["RUS", "KSA"],

	["EGY", "URU"],
	["MAR", "IRN"],
	["POR", "ESP"],

	["FRA", "AUS"],
	["ARG", "ICE"],
	["PER", "DEN"],
	["CRO", "NGA"],

	["CRC", "SRB"],
	["GER", "MEX"],
	["BRA", "SWI"],
	
	["SWE", "KOR"],
	["BEL", "PAN"],
	["TUN", "ENG"],

	["COL", "JPN"],
	["POL", "SEN"],
	["RUS", "EGY"],

	["POR", "MAR"],
	["URU", "KSA"],
	["IRN", "ESP"],

	["DEN", "AUS"],
	["FRA", "PER"],
	["ARG", "CRO"],

	["BRA", "CRC"],
	["NGA", "ICE"],
	["SRB", "SWI"],

	["BEL", "TUN"],
	["KOR", "MEX"],
	["GER", "SWE"],

	["ENG", "PAN"],
	["JPN", "SEN"],
	["POL", "COL"],

	["URU", "RUS"],
	["KSA", "EGY"],
	["ESP", "MAR"],
	["IRN", "POR"],

	["AUS", "PER"],
	["DEN", "FRA"],
	["NGA", "ARG"],
	["ICE", "CRO"],

	["KOR", "GER"],
	["MEX", "SWE"],
	["SRB", "BRA"],
	["SWI", "CRC"],

	["JPN", "POL"],
	["SEN", "COL"],
	["PAN", "TUN"],
	["ENG", "BEL"]
	]

def _build_games(teams):
	gs = []
	gs.append({teams[0],teams[1]})
	gs.append({teams[2],teams[3]})
	gs.append({teams[0],teams[2]})
	gs.append({teams[3],teams[1]})
	gs.append({teams[3],teams[0]})
	gs.append({teams[1],teams[2]})
	return gs


def _build_teams():
	ts = []
	for g in groups:
		ts += groups[g]
	return ts



groups = {
	"A": ["RUS", "KSA", "EGY", "URU"],
	"B": ["POR", "ESP", "MAR", "IRN"],
	"C": ["FRA", "AUS", "PER", "DEN"],
	"D": ["ARG", "ICE", "CRO", "NGA"],
	"E": ["BRA", "SWI", "CRC", "SRB"],
	"F": ["GER", "MEX", "SWE", "KOR"],
	"G": ["BEL", "PAN", "TUN", "ENG"],
	"H": ["POL", "SEN", "COL", "JPN"]
}

teams = sorted(_build_teams())


group_pairs = {
	"A": _build_games(groups["A"]),
	"B": _build_games(groups["B"]),
	"C": _build_games(groups["C"]),
	"D": _build_games(groups["D"]),
	"E": _build_games(groups["E"]),
	"F": _build_games(groups["F"]),
	"G": _build_games(groups["G"]),
	"H": _build_games(groups["H"])
}

if __name__ == "__main__":
	pprint.pprint(group_pairs)
	pprint.pprint(_build_teams())