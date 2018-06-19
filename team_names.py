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

team_en = {"RUS": "Russia",
"BRA": "Brazil",
"IRN": "Iran",
"JPN": "Japan",
"MEX": "Mexico",
"BEL": "Belgium",
"KOR": "South Korea",
"KSA": "Saudi Arabia",
"GER": "Germany",
"ENG": "England",
"ESP": "Spain",
"NGA": "Nigeria",
"CRC": "Costa Rica",
"POL": "Poland",
"EGY": "Egypt",
"ICE": "Iceland",
"SRB": "Serbia",
"POR": "Portugal",
"FRA": "France",
"URU": "Uruguay",
"ARG": "Argentina",
"COL": "Colombia",
"PAN": "Panama",
"SEN": "Senegal",
"MAR": "Morocco",
"TUN": "Tunisia",
"SWI": "Switzerland",
"CRO": "Croatia",
"SWE": "Sweden",
"DEN": "Denmark",
"AUS": "Australia",
"PER": "Peru"};

team_es = {"RUS": "Rusia",
"BRA": "Brasil",
"IRN": "Irán",
"JPN": "Japón",
"MEX": "México",
"BEL": "Bélgica",
"KOR": "Corea del Sur",
"KSA": "Arabia Saudita",
"GER": "Alemania",
"ENG": "Inglaterra",
"ESP": "España",
"NGA": "Nigeria",
"CRC": "Costa Rica",
"POL": "Polonia",
"EGY": "Egipto",
"ICE": "Islandia",
"SRB": "Serbia",
"POR": "Portugal",
"FRA": "Francia",
"URU": "Uruguay",
"ARG": "Argentina",
"COL": "Colombia",
"PAN": "Panamá",
"SEN": "Senegal",
"MAR": "Marruecos",
"TUN": "Túnez",
"SWI": "Suiza",
"CRO": "Croacia",
"SWE": "Suecia",
"DEN": "Dinamarca",
"AUS": "Australia",
"PER": "Perú"};

team_code = {'Russia': 'RUS',
 'Brazil': 'BRA',
 'Iran': 'IRN',
 'Japan': 'JPN',
 'Mexico': 'MEX',
 'Belgium': 'BEL',
 'South Korea': 'KOR',
 'Saudi Arabia': 'KSA',
 'Germany': 'GER',
 'England': 'ENG',
 'Spain': 'ESP',
 'Nigeria': 'NGA',
 'Costa Rica': 'CRC',
 'Poland': 'POL',
 'Egypt': 'EGY',
 'Iceland': 'ICE',
 'Serbia': 'SRB',
 'Portugal': 'POR',
 'France': 'FRA',
 'Uruguay': 'URU',
 'Argentina': 'ARG',
 'Colombia': 'COL',
 'Panama': 'PAN',
 'Senegal': 'SEN',
 'Morocco': 'MAR',
 'Tunisia': 'TUN',
 'Switzerland': 'SWI',
 'Croatia': 'CRO',
 'Sweden': 'SWE',
 'Denmark': 'DEN',
 'Australia': 'AUS',
 'Peru': 'PER',
 'Rusia': 'RUS',
 'Brasil': 'BRA',
 'Irán': 'IRN',
 'Japón': 'JPN',
 'México': 'MEX',
 'Belgica': 'BEL',
 'Corea del Sur': 'KOR',
 'Arabia Saudí': 'KSA',
 'Arabia Saudita': 'KSA',
 'Alemania': 'GER',
 'Inglaterra': 'ENG',
 'España': 'ESP',
 'Polonia': 'POL',
 'Egipto': 'EGY',
 'Islandia': 'ICE',
 'Francia': 'FRA',
 'Marruecos': 'MAR',
 'Túnez': 'TUN',
 'Suiza': 'SWI',
 'Croacia': 'CRO',
 'Suecia': 'SWE',
 'Dinamarca': 'DEN',
 'Perú': 'PER'}



def es(team_code):
	return team_es[team_code]

def en(team_code):
	return team_en[team_code]

def is_valid_code(team_code):
	return team_code in team_en

def to_team_name(team_code, lang="es"):
	if lang == "es":
		return es(team_code)
	else:
		return en(team_code)