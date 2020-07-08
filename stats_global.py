"""
Create charts for simulation CSVs
"""

import pathlib
import json
from libs.nodesreader import NodesReader
from libs.utils import ip2class

STATS = {"Simulation": "nodes.1",
         "Total": 0,
         "Classes": {
             "127": 0,
             "63": 0,
             "31": 0,
             "15": 0,
             "1": 0},
         }


if __name__ == "__main__":
    reader = NodesReader("NODES/nodes.1")
    for classe in reader.ip_classes:
        ip_count = reader.ip_classes[classe][0]
        STATS["Total"] += 1
        if ip_count >= 127:
            STATS["Classes"]["127"] += 1
        elif ip_count >= 63:
            STATS["Classes"]["63"] += 1
        elif ip_count >= 31:
            STATS["Classes"]["31"] += 1
        elif ip_count >= 15:
            STATS["Classes"]["15"] += 1
        else:
            STATS["Classes"]["1"] += 1
    print(STATS)
    with open("cache/nodes1.json", "w") as fp:
        json.dump(STATS, fp)
    # print(reader.ip_classes)

    CLASSES = {}
    with open("cache/whois.json") as fp:
        WHOIS = json.load(fp)
    for ip in WHOIS:
        ip_class = ip2class(ip)
        id = WHOIS[ip].split(',')
        country = id.pop()
        owner = ','.join(id)
        CLASSES[ip_class] = (owner.strip(), country.strip())
    OWNERS = {}
    COUNTRIES = {}
    for classe in reader.ip_classes:
        if classe in ['0.0.0', '127.0.0']:
            continue
        ip_count = reader.ip_classes[classe][0]
        owner, country = CLASSES[classe]
        if owner in OWNERS:
            OWNERS[owner] += ip_count
        else:
            OWNERS[owner] = ip_count
        if country in COUNTRIES:
            COUNTRIES[country] += ip_count
        else:
            COUNTRIES[country] = ip_count
    OWNERS = {k: OWNERS[k] for k in sorted(OWNERS, key=OWNERS.get, reverse=True)}
    # print(OWNERS)
    COUNTRIES = {k: COUNTRIES[k] for k in sorted(COUNTRIES, key=COUNTRIES.get, reverse=True)}
    # print(COUNTRIES)
    with open("cache/stats.json", "w") as fp:
        json.dump({"Owners": OWNERS, "Countries": COUNTRIES}, fp)
    with open("cache/owners.csv", "w") as fp:
        fp.write("Owner,Count\n")
        for owner in OWNERS:
            fp.write("{},{}\n".format(owner.replace(',',' '), OWNERS[owner]))
    with open("cache/countries.csv", "w") as fp:
        fp.write("Country,Count\n")
        for country in COUNTRIES:
            fp.write("{},{}\n".format(country.strip(','), COUNTRIES[country]))



