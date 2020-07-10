"""
Simulation with hashed c-class + end of last byte

- random hash (not questioned) - sha256 of a bitstring - 32 bytes
 Nyzo Score computation from hash of IP start to effectively reorder the various c-class and their gaps.
    Then complete the score with latest IP byte.
    That last IP byte is split in two:
        - first part is used
    Should be similar to first picking a single random c-class from the different c-classes + 4 last bits, then picking a 4 bits prefix that c-class
    gives full 256 c-classes 16 odds, and give small contiguous blocks in c-classes more odds, same as single c-classes.

"""


from libs.utils import random_hash
from libs.utils import hashed_class_mix_score, shuffle_mix
from libs.nodesreader import NodesReader


if __name__ == "__main__":
    readers = []
    for i in range(5):
        readers.append(NodesReader("NODES/nodes.{}".format(i+1)))
    # save_whois()

    for test in range(1000):
        cycle_hash = random_hash()
        shuffle_mix(cycle_hash)
        # print("Run {}".format(test))
        winners = []
        for i in range(5):
            winner = readers[i].winner(cycle_hash, scoring=hashed_class_mix_score)
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


