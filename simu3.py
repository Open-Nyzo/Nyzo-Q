"""
Simulation with lottery in ip space instead of identifier space.

- random hash (not questioned) - sha256 of a bitstring - 32 bytes
- first 4 bytes of hash are directly compared to ip bytes, so an ip in a dense ip regions (c-class) is less likely to win
- closest eligible ip is voted for

"""


from libs.utils import random_hash
from libs.utils import raw_ip_score, save_whois
from libs.nodesreader import NodesReader


if __name__ == "__main__":
    readers = []
    for i in range(5):
        readers.append(NodesReader("NODES/nodes.{}".format(i+1)))
    # save_whois()

    for test in range(1000):
        cycle_hash = random_hash()
        # print("Run {}".format(test))
        winners = []
        for i in range(5):
            winner = readers[i].winner(cycle_hash, scoring=raw_ip_score)
            ip_class = readers[i].verifiers[winner][1]
            ip_class_count = readers[i].ip_classes[ip_class][0]
            # print(winner.hex(), ip_class, ip_class_count)
            winners.append(winner)
        # exit()
        full = True
        for i in range(4):
            if winners[4] != winners[i]:
                full = False
        print("{},{},{},{}".format(test, full, ip_class, ip_class_count))


