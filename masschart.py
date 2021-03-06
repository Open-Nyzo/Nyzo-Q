"""
Create charts for simulation CSVs
"""

import json
import pathlib

SIMULATION = "current_lottery"
SIMULATION = "ip_lottery"
SIMULATION = "raw_ip_lottery"
SIMULATION = "shuffle_ip_lottery"
SIMULATION = "linear_ip_lottery"
SIMULATION = "linear_ip_lottery2"
SIMULATION = "linear_ip_lottery4"
SIMULATION = "linear_ip_lottery5"
SIMULATION = "linear_ip_lottery4b"
SIMULATION = "hashed_class"
SIMULATION = "hashed_class_mix"
SIMULATION = "hashed_class_v2"

DIR = pathlib.Path('./simulations/{}/mass'.format(SIMULATION))

STATS = {"Simulation": SIMULATION,
         "Total": 0,
         "Queue": {},
         "Classes": {
             "127": 0,
             "63": 0,
             "31": 0,
             "15": 0,
             "1": 0},
         "Classes_PC": {},
         "Classes_global_PC": {}
         }


def process(file_name):
    global STATS
    with open(file_name) as fp:
        for line in fp:
            if "DIVERGE" in line:
                continue
            try:
                ip, ip_class, ip_count = line.strip().split(",")
            except:
                continue
            STATS["Total"] += 1
            ip_count = int(ip_count)
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


if __name__ == "__main__":
    with open("cache/nodes1.json") as fp:
        STATS["Queue"] = json.load(fp)['Classes']
    with open("cache/nodes1.json") as fp:
        total_classes_in_queue = json.load(fp)['Total']

    for file_name in DIR.glob("*.csv"):
        process(file_name)
    for classe in ("127", "63", "31", "15", "1"):
        STATS["Classes_PC"][classe] = "{:0.2f}".format(STATS["Classes"][classe] / STATS["Total"] * 100)

        STATS["Classes_global_PC"][classe] = "{:0.4f}".format(float(STATS["Classes_PC"][classe]) / STATS["Queue"][classe])

    print(STATS)
    with open('./simulations/{}/mass/stats.json'.format(SIMULATION), "w") as fp:
        json.dump(STATS, fp)
