# 301060 - FIFA World Cup 2018 Simulator

This repository contains the simulator used for obtaining the results in https://301060.exactas.uba.ar. This repository *does not* contain the mathematical models and R scripts used for deriving the probabilities, it simply a simulator that uses those probabilities as input to simulate the tournament. See the website for some discussion about the mathematical models used. 

## Requirements

- MongoDB
- Python3

## Usage

The main files are `cachablesimulator.py` and `matchloader.py`. The first one is a wrapper for the simulator written in `simulator.py` that enables one to store simulations in a mongoDB (no one wants to wait 10 extra minutes for a simulation already done). The second file is the one you must play around with to store some already-played matches in the mongoDB database. 

The work flow is expected to be as follows:
1. you store some played matches with `MatchLoader`
2. you run a simulation with `CachableSimulator` as follows (in python3):
```python
gms = MatchLoader.load_group_matches() # a list
kms = MatchLoader.load_knockout_matches() # a dict
c = CachableSimulator(gms, kms) # it simulates and stores the simulation (or loads it if possible)
```
3. you play around with the output of the simulator (see `simulator.py` to get an idea of the interface of `CachableSimulator`).

We used 1M iterations for every simulation, but you can adjust that number in `config.py`.

The MongoDB database is called worldcup18, and the collections used are `simulations`, `group_matches` and `knockout_matches`.
## Credits
- Mathematical models were developed by Iván Monardo, Federico Bertero, Facundo Gutiérrez and Guillermo Durán.
- The code of the simulator that uses the output of those models was written by Saveliy Vasiliev (the contents of the current repository).
- Other collaborators of the 301060 project: Min Chih Lin, Armando Doria, Flavia Bonomo, Irene Fernández, Paula Bassi, Gabriel Rocca, Pablo Groisman, Andrés Farall, Juan Ruiz, Florencia Fernández Slezak and Pablo Lobato.
