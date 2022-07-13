import os
import sys
import json
import tqdm
import re
from scipy.spatial import distance


def get_system_pos(system_name, systems):
    for system in systems:
        if system_name == system["name"]:
            return (system['x'], system['y'], system['z'])

def has_expansion_state(system):
    for faction in system["minor_faction_presences"]:
        for state in faction["active_states"]:
            if state["name"] == "Expansion":
                return True

def get_system_distance(target_system, refference_vector):
    return distance.euclidean(
        (target_system["x"], target_system["y"], target_system["z"]),
        refference_vector
    )

def get_viable_stations(systems, stations, refference_vector):
    viable = []
    for system in tqdm.tqdm(systems):
        if has_expansion_state(system):
            for station in stations:
                if station["system_id"] == system["id"] and station["is_planetary"] == False:
                    if any(x["name"] == "Expansion" for x in station["states"]):
                        if ("Industrial" in station["economies"]) and (not all(x in station["economies"] for x in ["Extraction", "Refinery", "Terraforming"])):
                            viable.append((station["name"], system["name"], get_system_distance(system, refference_vector)))
    return viable


if __name__ == "__main__":
    arguments = ' '.join(sys.argv[1:])

    systems_file = open("systems_populated.json", "r")
    stations_file = open("stations.json", "r")
    systems = json.load(systems_file)
    stations = json.load(stations_file)
    systems_file.close()
    stations_file.close()

    refference_system_pos = get_system_pos(arguments, systems)
    if not refference_system_pos:
        print(f"No system found with name {arguments}\n(Are you sure the capitalization is correct?)")
        exit(2)
        
    viable = get_viable_stations(systems, stations, refference_system_pos)
    viable.sort(key=lambda tup: tup[2])
    
    os.remove("viable_stations.txt")
    with open("viable_stations.txt", 'w') as output:
        for tup in viable:
            output.write(f"{tup[0]} in {tup[1]} and {tup[2]}Ly away\n")
