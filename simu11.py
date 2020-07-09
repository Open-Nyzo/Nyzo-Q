"""
Simulation with lottery in shuffled linear ip space

- random hash (not questioned) - sha256 of a bitstring - 32 bytes
- first 4 bytes of hash are converted to an int.
- ip is converted to a 4 bytes int as well
    Shuffle a,b,c order from a.b.c.d to effectively reorder the various c-class and their gaps.
    When two candidates (before and after) have same score, give preference to the right one.
    Should be similar to first picking a single random c-class from the different c-classes, then picking a single ip from that c-class
- same table is used for all 4 bytes in turn.
- closest eligible ip is voted for

"""


from libs.utils import random_hash
from libs.utils import hashed_class_score, shuffle
from libs.nodesreader import NodesReader


if __name__ == "__main__":
    readers = []
    for i in range(5):
        readers.append(NodesReader("NODES/nodes.{}".format(i+1)))
    # save_whois()

    for test in range(1000):
        cycle_hash = random_hash()
        shuffle(cycle_hash)
        # print("Run {}".format(test))
        winners = []
        for i in range(5):
            winner = readers[i].winner(cycle_hash, scoring=hashed_class_score)
            ip_class = readers[i].verifiers[winner][1]
            ip_class_count = readers[i].ip_classes[ip_class][0]
            # print(winner.hex(), ip_class, ip_class_count)
            winners.append(winner)
        # exit()
        full = True
        for i in range(4):
            if winners[4] != winners[i]:
                full = False
        if not full:
            print(cycle_hash.hex(), 'DIVERGE')
        print("{},{},{},{}".format(test, full, ip_class, ip_class_count))


