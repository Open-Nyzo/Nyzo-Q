"""
Simulation with close to current process:

- random hash (not questioned) - sha256 of a bitstring - 32 bytes, like identifier.
- closest eligible node is voted for

"""


from libs.utils import random_hash
from libs.nodesreader import NodesReader


if __name__ == "__main__":
    readers = []
    for i in range(5):
        readers.append(NodesReader("NODES/nodes.{}".format(i+1)))

    for test in range(10):
        cycle_hash = random_hash()
        # print("Run {}".format(test))
        winners = []
        for i in range(5):
            winner = readers[i].winner(cycle_hash)
            ip_class = readers[i].verifiers[winner][1]
            ip_class_count = readers[i].ip_classes[ip_class][0]
            #print(winner.hex(), ip_class, ip_class_count)
            winners.append(winner)
        full = True
        for i in range(4):
            if winners[4] != winners[i]:
                full = False
        print("{},{},{},{}".format(test, full, ip_class, ip_class_count))


