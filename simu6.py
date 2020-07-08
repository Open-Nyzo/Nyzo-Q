"""
Simulation with lottery in shuffled linear ip space

- random hash (not questioned) - sha256 of a bitstring - 32 bytes
- first 4 bytes of hash are converted to an int.
- ip is converted to a 4 bytes int as well
- first 2 bytes of ip are shuffled via a pseudo random lookup table, fed from the hash, to account for non uniform density in public ip v4
- closest eligible ip is voted for

"""


from libs.utils import random_hash
from libs.utils import linear_ip_score2, shuffle
from libs.nodesreader import NodesReader


if __name__ == "__main__":
    readers = []
    for i in range(5):
        readers.append(NodesReader("NODES/nodes.{}".format(i+1)))
    # save_whois()

    for test in range(10000):
        cycle_hash = random_hash()
        shuffle(cycle_hash)
        # print("Run {}".format(test))
        winners = []
        for i in range(5):
            winner = readers[i].winner(cycle_hash, scoring=linear_ip_score2)
            ip_class = readers[i].verifiers[winner][1]
            ip_class_count = readers[i].ip_classes[ip_class][0]
            # print(winner.hex(), ip_class, ip_class_count)
            winners.append(winner)
        # exit()
        full = True
        for i in range(4):
            if winners[4] != winners[i]:
                full = False
                print(cycle_hash.hex(), 'DIVERGE')
        print("{},{},{},{}".format(test, full, ip_class, ip_class_count))


