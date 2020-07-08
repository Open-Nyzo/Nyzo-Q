"""
Helpers
"""

from hashlib import sha256
import json
import socket
import sys
from random import getrandbits, Random
from ipwhois import IPWhois
import warnings

WHOIS = None


def warn(*args, **kwargs):
    pass


warnings.warn = warn


SHUFFLE_MAP = []


def current_score(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation, see
    https://github.com/n-y-z-o/nyzoVerifier/blob/75786060a822443154bcdaaa371fe8696d54a201/src/main/java/co/nyzo/verifier/NewVerifierQueueManager.java#L214
    """
    score = sys.maxsize
    if len(cycle_hash) != 32 or len(identifier) != 32:
        return score

    combined_array = b''
    for i in range(32):
        combined_array += ((cycle_hash[i] + identifier[i]) & 0xff).to_bytes(1, byteorder='big')
    hashed_identifier = sha256(combined_array).digest()

    score = 0
    for i in range(32):
        hash_value = cycle_hash[i] & 0xff
        identifier_value = hashed_identifier[i] & 0xff
        score += abs(hash_value - identifier_value)
    return score


def ip_score(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation from ip distance
    """
    score = sys.maxsize
    if ip == '':
        return score

    combined_array = b''
    ip_bytes = socket.inet_aton(ip)
    for i in range(4):
        combined_array += ((cycle_hash[i] + ip_bytes[i]) & 0xff).to_bytes(1, byteorder='big')
    hashed_ip = sha256(combined_array).digest()

    score = 0
    for i in range(32):
        hash_value = cycle_hash[i] & 0xff
        ip_value = hashed_ip[i] & 0xff
        score += abs(hash_value - ip_value)
    # print(ip, ip_bytes.hex(), hashed_ip.hex(), score)
    return score


def shuffle_ip_score(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation from xor'd c class ip distance
    """
    score = sys.maxsize
    if ip == '':
        return score

    ip_bytes = socket.inet_aton(ip)

    score = 0
    for i in range(3):
        hash_value = cycle_hash[i]
        ip_value = cycle_hash[i] ^ ip_bytes[i]
        score += abs(hash_value - ip_value)
    score += abs(cycle_hash[3] - ip_bytes[3])
    # print(ip, score)
    return score


def raw_ip_score(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation from raw ip distance
    """
    score = sys.maxsize
    if ip == '':
        return score

    ip_bytes = socket.inet_aton(ip)
    score = 0
    for i in range(4):
        hash_value = cycle_hash[i]
        ip_value = ip_bytes[i]
        score += abs(hash_value - ip_value)
    # print(ip, ip_bytes.hex(), hashed_ip.hex(), score)
    return score


def linear_ip_score(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation from raw ip distance in linear space
    Possible side effect with high or low ip ranges?
    """
    score = sys.maxsize
    if ip == '':
        return score

    ip_bytes = socket.inet_aton(ip)
    ip_int = int.from_bytes(ip_bytes, "big")
    hash_int = int.from_bytes(cycle_hash[:4], "big")
    score = abs(hash_int - ip_int)
    # print(ip, ip_int, cycle_hash[:4].hex(), hash_int, score)
    return score


def shuffle(cycle_hash: bytes):
    global SHUFFLE_MAP
    SHUFFLE_MAP = [i for i in range(256)]
    random = Random(cycle_hash)
    random.shuffle(SHUFFLE_MAP)
    # print(SHUFFLE_MAP)


def shuffle4(cycle_hash: bytes):
    global SHUFFLE_MAP
    SHUFFLE_MAP = []
    random = Random(cycle_hash)
    for i in range(4):
        map = [i for i in range(256)]
        random.shuffle(map)
        SHUFFLE_MAP.append(list(map))  # copy, not reference
    # print(SHUFFLE_MAP)


def linear_ip_score2(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation from raw ip distance in linear space, with 2 first bytes being pseudo randomly shuffled
    Possible side effect with high or low ip ranges?
    """
    score = sys.maxsize
    if ip == '':
        return score

    ip_bytes = socket.inet_aton(ip)
    ip_bytes_shuffle = (SHUFFLE_MAP[ip_bytes[0]]).to_bytes(1, byteorder='big')
    ip_bytes_shuffle += (SHUFFLE_MAP[ip_bytes[1]]).to_bytes(1, byteorder='big')
    ip_bytes_shuffle += ip_bytes[2:]
    ip_int = int.from_bytes(ip_bytes_shuffle, "big")
    # shuffled = socket.inet_ntoa(ip_bytes_shuffle)
    hash_int = int.from_bytes(cycle_hash[:4], "big")
    score = abs(hash_int - ip_int)
    # print(ip, ip_bytes, ip_bytes_shuffle, shuffled, cycle_hash[:4].hex(), hash_int, score)
    # sys.exit()
    return score


def linear_ip_score4(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation from raw ip distance in linear space, with allt bytes being pseudo randomly shuffled with same permutation map
    """
    score = sys.maxsize
    if ip == '':
        return score

    ip_bytes = socket.inet_aton(ip)
    """
    ip_bytes_shuffle = (SHUFFLE_MAP[ip_bytes[0]]).to_bytes(1, byteorder='big')
    ip_bytes_shuffle += (SHUFFLE_MAP[ip_bytes[1]]).to_bytes(1, byteorder='big')
    ip_bytes_shuffle += (SHUFFLE_MAP[ip_bytes[2]]).to_bytes(1, byteorder='big')
    ip_bytes_shuffle += (SHUFFLE_MAP[ip_bytes[3]]).to_bytes(1, byteorder='big')
    ip_int = int.from_bytes(ip_bytes_shuffle, "big")
    """
    ip_int = SHUFFLE_MAP[ip_bytes[0]] * 256 * 256 * 256\
             + SHUFFLE_MAP[ip_bytes[1]] * 256 * 256\
             + SHUFFLE_MAP[ip_bytes[2]] * 256 \
             + SHUFFLE_MAP[ip_bytes[3]]
    hash_int = int.from_bytes(cycle_hash[:4], "big")
    score = abs(hash_int - ip_int)
    return score


def linear_ip_score5(cycle_hash: bytes, identifier: bytes, ip: str) -> int:
    """
    Nyzo Score computation from raw ip distance in linear space, with all bytes being pseudo randomly shuffled with a different permutation map each
    """
    score = sys.maxsize
    if ip == '':
        return score

    ip_bytes = socket.inet_aton(ip)
    ip_int = SHUFFLE_MAP[0][ip_bytes[0]] * 256 * 256 * 256\
             + SHUFFLE_MAP[1][ip_bytes[1]] * 256 * 256\
             + SHUFFLE_MAP[2][ip_bytes[2]] * 256 \
             + SHUFFLE_MAP[3][ip_bytes[3]]
    hash_int = int.from_bytes(cycle_hash[:4], "big")
    score = abs(hash_int - ip_int)
    return score


def random_hash() -> bytes:
    """Let say this is a cycle hash"""
    random = getrandbits(1024).to_bytes(1024//8, byteorder='big')
    # print(random)
    return sha256(random).digest()


def identifier_to_bytes(identifier: str) -> bytes:
    return bytes.fromhex(identifier.replace('-',''))


def ip2class(ip: str) -> str:
    return '.'.join(ip.split(".")[:3])


def ip_whois(ip: str) -> str:
    global WHOIS
    if WHOIS is None:
        with open("cache/whois.json") as fp:
            WHOIS = json.load(fp)
    if ip in['127.0.0.1', '0.0.0.0']:
        return "localhost"
    if ip in WHOIS:
        return WHOIS[ip]
    try:
        obj = IPWhois(ip)
        res = obj.lookup_whois()
        desc = res.get("asn_description")
        WHOIS[ip] = desc
    except Exception as e:
        print(str(e))
        desc = ""
    print(desc)
    # sys.exit()
    return desc


def save_whois():
    if WHOIS is None:
        return
    with open("cache/whois.json", "w") as fp:
        json.dump(WHOIS, fp)


