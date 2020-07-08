"""
Simulation with lottery in shuffled linear ip space

- random hash (not questioned) - sha256 of a bitstring - 32 bytes
- first 4 bytes of hash are converted to an int.
- ip is converted to a 4 bytes int as well
- first 2 bytes of ip are shuffled via a pseudo random lookup table, fed from the hash, to account for non uniform density in public ip v4
- closest eligible ip is voted for

Many draws on a single "nodes" file, to analyse odds and bias.
"""


from libs.utils import random_hash
from libs.utils import linear_ip_score2, shuffle
from libs.nodesreader import NodesReader


if __name__ == "__main__":
    reader = NodesReader("NODES/nodes.1")
    # save_whois()

    for test in range(100000):
        cycle_hash = random_hash()
        shuffle(cycle_hash)
        # print("Run {}".format(test))
        winner = reader.winner(cycle_hash, scoring=linear_ip_score2)
        ip, ip_class = reader.verifiers[winner][:2]
        ip_class_count = reader.ip_classes[ip_class][0]
        print("{},{},{}".format(ip, ip_class, ip_class_count))


