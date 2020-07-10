"""
Nyzo Nodes file reader
"""

from libs.utils import identifier_to_bytes, ip2class, ip_whois
from libs.utils import current_score, ip_score
from sys import maxsize
import socket

class NodesReader:

    def __init__(self, filename: str):
        """Loads nodes file into memory and index by identifier and c ip class"""
        self.verifiers = {}
        self.ip_classes = {}
        with open(filename) as f:
            for line in f:
                verifier, ip, tcp, udp, queue_ts, void, inactive_ts = line.strip().split(":")
                if inactive_ts == '-1':
                    verifier_bytes = identifier_to_bytes(verifier)
                    ip_class = ip2class(ip)
                    ip_bytes = bytearray(socket.inet_aton(ip))  # pre-calc for perfs reasons.
                    # print(verifier_bytes.hex(), ip, ip_class, tcp, udp, queue_ts, void, inactive_ts)
                    self.verifiers[verifier_bytes] = [ip, ip_class, ip_bytes, False, False]
                    if ip_class in self.ip_classes:
                        self.ip_classes[ip_class][0] += 1
                        self.ip_classes[ip_class][1].append((verifier_bytes, ip))
                    else:
                        whois = ip_whois(ip)
                        # whois = ""
                        self.ip_classes[ip_class] = [1, [(verifier_bytes, ip)], whois]

    def winner(self, cycle_hash: bytes, scoring=None)-> bytes:
        """Simplified version of calculateVoteLotteryMethod() for all nodes of the file,
        regardless of their timestamp"""
        if scoring is None:
            scoring = current_score
        winning_score = maxsize
        winning_identifier = b''
        for verifier in self.verifiers:
            score = scoring(cycle_hash, verifier, self.verifiers[verifier][0], self.verifiers[verifier][2])
            # print(verifier.hex(), score)
            if score < winning_score:
                winning_score = score
                winning_identifier = verifier
        return winning_identifier

    def calc_ends(self):
        """Parse data and add flags for "first in range" and "last in range", to estimate bias"""
        pass



