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

import random
import pprint
import estimations_data as data

result_order = [[5,0],[5,1],[5,2],[5,3],[5,4],[4,0],[4,1],[4,2],[4,3],[3,0],[3,1],[3,2],[2,0],[2,1],[1,0],[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[0,1],[1,2],[0,2],[2,3],[1,3],[0,3],[3,4],[2,4],[1,4],[0,4],[4,5],[3,5],[2,5],[1,5],[0,5]]


def random_score(team1, team2):
	r = random.uniform(0,1) 

	if team1 in data.accumulated and team2 in data.accumulated[team1]:
		accumulated = data.accumulated[team1][team2]
		result_index = next(i for i, v in enumerate(accumulated) if v >= r)
		return dict(zip([team1, team2], result_order[result_index][:]))
	else:
		accumulated = data.accumulated[team2][team1]
		result_index = next(i for i, v in enumerate(accumulated) if v >= r)
		return dict(zip([team1, team2], result_order[result_index][::-1]))


def result_matrix(team1, team2):
	d = dict(zip([0,1,2,3,4,5], [{} for _ in range(6)]))
	prob_row, row_ord = _get_prob_row_and_order(team1, team2)
	for i, result in enumerate(row_ord):
		d[result[0]][result[1]] = prob_row[i]
	return d

def _get_prob_row_and_order(team1, team2):
	for row in data.prob_ivan:
		if team1 == row[0] and team2 == row[1]:
			return row[2:], result_order[:]
		elif team1 == row[1] and team2 == row[0]:
			return row[2:], [l[::-1] for l in result_order]


def _build_accumulated_probs():
	acc = {}
	for p in data.prob_ivan:
		if p[0] not in acc:
			acc[p[0]] = {} 
		raw_accum = [sum(p[2:i+3]) for i in range(len(p)-2)] # norm
		acc[p[0]][p[1]] = [a/raw_accum[-1] for a in raw_accum]
	return acc


if __name__ == "__main__":
	for i in range(100):
		print(random_score("ARG", "KSA"))
		print(random_score("KSA", "ARG"))

	print("\nRUS vs KSA result matrix:")
	pprint.pprint(result_matrix("RUS", "KSA"))
	pprint.pprint(result_matrix("RUS", "JPN"))