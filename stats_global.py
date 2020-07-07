"""
Create charts for simulation CSVs
"""

import pathlib

SIMULATION = "current_lottery"
SIMULATION = "ip_lottery"
SIMULATION = "raw_ip_lottery"


DIR = pathlib.Path('./simulations/{}'.format(SIMULATION))

STATS = {"Simulation": SIMULATION,
         "Total": 0, "Consensus": 0,
         "Classes": {
             "127": 0,
             "63": 0,
             "31": 0,
             "15": 0,
             "1": 0},
         "Classes_PC": {}
         }


def process(file_name):
    global STATS
    with open(file_name) as fp:
        for line in fp:
            _, consensus, ip_class, ip_count = line.strip().split(",")
            STATS["Total"] += 1
            ip_count = int(ip_count)
            if consensus == 'True':
                STATS["Consensus"] += 1
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

    for file_name in DIR.glob("*.csv"):
        process(file_name)
    STATS["Consensus_PC"] = "{:0.2f}".format(STATS["Consensus"] / STATS["Total"] * 100)
    for classe in ("127", "63", "31", "15", "1"):
        STATS["Classes_PC"][classe] =  "{:0.2f}".format(STATS["Classes"][classe] / STATS["Total"] * 100)

    print(STATS)
