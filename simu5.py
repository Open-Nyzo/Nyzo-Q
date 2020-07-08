"""
Simulation with lottery in linear ip space

- random hash (not questioned) - sha256 of a bitstring - 32 bytes
- first 4 bytes of hash are converted to an int.
- ip is converted to a 4 bytes int as well
- closest eligible ip is voted for

"""


from libs.utils import random_hash
from libs.utils import linear_ip_score, save_whois
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
            winner = readers[i].winner(cycle_hash, scoring=linear_ip_score)
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


"""
ee0ca66b98f98bb4da96efc526c2aaa0c4de317f8e23dd5b0cba2b765e45ba86 DIVERGE
0366d56dfba7223fe92b1d24448128db8a84a309d4a4d2eeaf474810387f5ef0 DIVERGE
ece4279b1b6f9d14f324a2c6c650bd568d4fdf35e259859585786c2f7c1b106c DIVERGE
f547ae6254c56b23b6b96515a6b9d4d04003878e6aace550a7f57ce8d3c5c3f1 DIVERGE
e5e6d895e3e27ae0224b7fc20902e184841748b40a912666e2794988f79bb53e DIVERGE
"""
