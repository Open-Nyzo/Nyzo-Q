"""
Many draws on a single "nodes" file, to analyse odds and bias.
"""


from libs.utils import random_hash
from libs.utils import linear_ip_score4_plus, shuffle_plus
from libs.nodesreader import NodesReader


if __name__ == "__main__":
    reader = NodesReader("NODES/nodes.1")
    # save_whois()

    for test in range(100000):
        cycle_hash = random_hash()
        shuffle_plus(cycle_hash)
        # print("Run {}".format(test))
        winner = reader.winner(cycle_hash, scoring=linear_ip_score4_plus)
        ip, ip_class = reader.verifiers[winner][:2]
        ip_class_count = reader.ip_classes[ip_class][0]
        print("{},{},{}".format(ip, ip_class, ip_class_count))


