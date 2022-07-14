# Elite Dangerous Mining Expansion Finder
A tool that finds stations with the following criteras:
- Want:
  - Faction state: Expansion
  - Economy: Industrial
- Don't want:
  - Economy: Extraction, Refinery, Terraforming
  - Settlements (planetary stations)
and then sorts them by Ly to a specified refference system

# Usage
1. Install [PyPy](https://www.pypy.org/) or [Python 3+](https://www.python.org/downloads/) (PyPy is recommended as it is a LOT faster). Install curl (google it for your specific distro/os)
2. Install python dependencies with: `pip install -r requirements.txt`
3. - Linux: Run the `run.sh` script, and provide it the system name (it's case sensitive).
   - Windows: Too lazy to make scripts for windows too, but you can just download the 2 needed files from [EDDB API](https://eddb.io/api) (you should do this every day if you plan to run the script often), then run the python script manually, also providing the system name (it's case sensitive).
  
# Notes
- I'm using the [EDDB system dumps](https://eddb.io/api), namely `systems_populated.json` and `stations.json`
- You may get inconsistent results after [the tick](https://elite-dangerous.fandom.com/wiki/Background_Simulation) happens, because data is mostly collected and uploaded by users using the [ED Discovery tool](https://github.com/EDDiscovery/EDDiscovery/wiki). So if none goes there with the tool open, the dumps will have the outdated, not updated factions in them.
