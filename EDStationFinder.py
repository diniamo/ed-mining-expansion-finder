import os
import sys
import json
import tqdm
from scipy.spatial import distance
import csv


def get_system_pos(system_name, systems):
    for system in systems:
        if system_name == system["name"]:
            return (system['x'], system['y'], system['z'])

def get_expansion_faction_id(system):
    for faction in system["minor_faction_presences"]:
        for state in faction["active_states"]:
            if state["name"] == "Expansion":
                return faction["minor_faction_id"] 
    return None

def get_system_distance(target_system, refference_vector):
    return distance.euclidean(
        (target_system["x"], target_system["y"], target_system["z"]),
        refference_vector
    )

def get_faction(faction_id, factions):
    for faction in factions:
        if faction["id"] == faction_id:
            return faction

def get_viable_stations(systems, stations, factions,  refference_vector):
    viable = []
    for system in tqdm.tqdm(systems):
        expansion_faction_id = get_expansion_faction_id(system)
        if expansion_faction_id != None:
            for station in stations:
                if station["system_id"] == system["id"] and station["type"] != "Fleet Carrier" and station["is_planetary"] == False:
                    if any(x["name"] == "Expansion" for x in station["states"]) and ("Industrial" in station["economies"]) and not any(x in station["economies"] for x in ["Extraction", "Refinery", "Terraforming"]):
                        faction = get_faction(expansion_faction_id, factions)
                        viable.append((system["name"], station["name"], get_system_distance(system, refference_vector), station["distance_to_star"], faction["name"], faction["allegiance"]))
    return viable


if __name__ == "__main__":
    arguments = ' '.join(sys.argv[1:])

    systems_file = open("systems_populated.json", "r")
    stations_file = open("stations.json", "r")
    factions_file = open("factions.json", "r")
    systems = json.load(systems_file)
    stations = json.load(stations_file)
    factions = json.load(factions_file)
    systems_file.close()
    stations_file.close()
    factions_file.close()

    refference_system_pos = get_system_pos(arguments, systems)
    if not refference_system_pos:
        print(f"No system found with name {arguments}\n(Are you sure the capitalization is correct?)")
        exit(2)
        
    viable = get_viable_stations(systems, stations, factions, refference_system_pos)
    viable.sort(key=lambda tup: tup[2])
    
    os.remove("viable_stations.csv")
    with open("viable_stations.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["System", "Station", f"Distance from {arguments} (Ly)", "Distance from star (Ls)", '', "Faction name", "Faction allegiance"])
        for tup in viable:
            writer.writerow([tup[0], tup[1], tup[2], tup[3], '', tup[4], tup[5]])
