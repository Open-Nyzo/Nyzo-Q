# Nyzo-Q

Nyzo Queue issues, tests and practical proposals.  

This repo is under active development. Posting in current raw state anyway, under the Unlicence.

## Current Nyzo queue issues

Current Queue displays 2 issues, related to heavy queue cost optimizations.  

- Unreachable verifiers, non stock or running part time, merely spamming nodejoins  
  (not dealt with here - Will be the subject of a github issue)
- Large groups of ips all owned by a very few entities (A few/single large OVH customers, One Ukrainian ISP with 6000 ips, Amazon)

The large ip classes owned by a few owners represents like 0.5% of all ip groups but do account for 50% of new node joins.  
This is happening since months (*insert first seen timestamp of full c-class*) and is growing. 
As a result, the diversity of in-cycle verifier can not be assumed anymore and the recent NCFP-10 votes (can't reach 50% "YES", but no "NO") is quite worrysome. 

*insert table from open nyzo*

Instead of "proof of diversity", Nyzo queue in fact now runs a "proof of quantity".

It's time to wonder if nyzo aims to be run by a few large operators, or wants to give control and chances back to individuals.

> See cache/countries.csv and cache/owners.csv for current repartition of queue ip, built by stats_global.py

## Current lottery

Current lottery mechanism relies on the fact that queue nodes need a unique ip, however that ip is **not** used at all in the scoring process.    
Only the verifier id is used after some hashing.

Thus, the more IPs you own - no matter their *diversity* - the more chances you have.   

Imagine a lottery wheel, where every eligible ip has the same size and chance to win. Double the IPs, all size are divided by 2, every eligible ip has the same chance.

The drawback of this is encouraging IP cost optimization, no matter the diversity.  

- Big players end up on the cheapest recurring cost provider (OVH, setup fees but no recurring)
- Some players do use IPs they already own for other purposes (ISP, but also any service provider needing ip for existing services like proxies, vpn, scraping, bots...)

Looking at the queue, this is obvious: on a regular vps provider, where clients do rent vps and ips, you may have a few ip per c-class running a verifier.  
On big players verifiers, you have full blocks of 32, 64, 128 and 256 or more contiguous ips with queue verifiers.

## My approach

To ensure in-cycle diversity, we have to favor in-queue diversity.    
We don't want KYC or one person - one node, we just want stronger guarantees that the queue - hence the cycle - is diverse.
  
c-class (or smaller) filled with queue verifiers are the track left by a few big players.  
This can be mitigated by scoring on ip data, not just random verifier identifier.

Imagine a lottery wheel, where every possible ip is drawn. Some parts are dense in queue verifiers (full c-class), other are sparse (regular vps users, home users)  
When you spin the wheel, either you end up on a lucky queue ip directly, either the closest queue ip is the winner.

This lottery is based upon ip diversity, no more ip quantity. 
You still have more chances if you have more ips, but you don't end up with the same leverage as now.

Such a lottery, instead of concentrating all queue nodes to OVH and a few service providers, incitates to use many various providers instead, and gives regular users their chances to join the cycle.

## The concerns

It's all a question of balance.  
Current lottery removes all bias in verifier data.  
If we remove all bias in ips structure as well, we can no more ensure diversity and we go back to quantity only.

The thing is to find the good balance between diversity and bias. Roughly: how to draw all possible ips on the wheel so that everyone gets a fair chance, and diversity still is ensured.

## Simulations

Nyzo does not have a consensus on the queue nodes.  
Every in-cycle verifier has its own list of queue nodes, with related ip and first seen timestamp.  
This makes it harder to elect a common verifier in a safe way, since 2 different in-cycle will have a different queue list and data.

To account for that and make sure the various options do not add more scattering, I ran simulations from 5 nodes files from 5 different in-cycles nodes.  
This can be run on more than that of course.

### current_lottery

see simulations/current_lottery/stats.json and related CSVs
```
{
  "Simulation": "current_lottery",
  "Total": 20000, "Consensus": 19718,
  "Consensus_PC": "98.59",
  "Queue": {"127": 64, "63": 28, "31": 45, "15": 17, "1": 6221},
  "Classes": {"127": 10236, "63": 1682, "31": 1311, "15": 261, "1": 6510},
  "Classes_PC": {"127": "51.18", "63": "8.41", "31": "6.55", "15": "1.31", "1": "32.55"},
  "Classes_global_PC": {"127": "0.80", "63": "0.30", "31": "0.15", "15": "0.08", "1": "0.01"},
}
```

**Total**: 20000 - Number of entry simulations
**Consensus** and **Consensus_PC**: how many times the 5 different nodes files gave the same winner.

> Note: this can't be 100% and does not need to. New entrant can be voted in even if all do not agree. If votes are split 50/50 between two winners, then after 50 blocks a new lottery will take place anyway.

**Queue**: How many queue candidates for each class in the first node file.    
- "1" is a group of 1 to 14 ips in their c-class
- "15" is a group of 15 to 30 ips in their c-class
- "31" is a group of 31 to 62 ips in their c-class
- "63" is a group of 63 to 126 ips in their c-class
- "127" is a group of 127 to 256 ips in their c-class  
We can see that classes with less than 15 ips per c-class are the vast majority (6221 classes).    
classes with 127 and up ips are low (64) but account for a lot of ips (64*256).  
This data is the same for all simulations and lottery mechanisms.

**Classes**: How many winners for each class.  

**Classes_PC**: % of times an ip of that class won.

**Classes_global_PC**: individual odd for an ip of that class to win.  
Here, if you have an average ip that is in the 127 class (say, one ip from a full c-class) then you have 0.08% odds to win.  
If you have an ip in the "1" class, majority one, you only have 0.01% chances.

**Current lottery and queue favors quantity over quality by a factor 8** 

> Note: sim.csv line content: index, Consensus(True|False), C-Class Winner, Number of IPs in that class

Current lottery scoring is ported from official nyzo code

```
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
```

### ip_lottery

See simulations/ip_lottery/stats.json and related CSVs

```
{"Simulation": "ip_lottery",
  "Total": 1000, "Consensus": 987,
  "Consensus_PC": "98.70",
  "Queue": {"127": 64, "63": 28, "31": 45, "15": 17, "1": 6221},
  "Classes": {"127": 523, "63": 77, "31": 39, "15": 17, "1": 344},
  "Classes_PC": {"127": "52.30", "63": "7.70", "31": "3.90", "15": "1.70", "1": "34.40"},
  "Classes_global_PC": {"127": "0.82", "63": "0.28", "31": "0.09", "15": "0.10", "1": "0.01"},
  }
```

Scoring similar to the current scoring, but on ip rather than verifier id

```
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
    return score
```

This is a "control" simulation. Since ip bytes are fuzzed before the distance computation, no order stands and large or small ip classes are not distinguishable.  
Thus, the stats are alike the current lottery, still in favor of quantity.


### raw_ip_lottery

See simulations/raw_ip_lottery/stats.json and related CSVs

```
{"Simulation": "raw_ip_lottery",
  "Total": 20000, "Consensus": 19528,
  "Consensus_PC": "97.64"
  "Queue": {"127": 64, "63": 28, "31": 45, "15": 17, "1": 6221},
  "Classes": {"127": 1732, "63": 380, "31": 555, "15": 252, "1": 17081},
  "Classes_PC": {"127": "8.66", "63": "1.90", "31": "2.77", "15": "1.26", "1": "85.41"},
  "Classes_global_PC": {"127": "0.14", "63": "0.07", "31": "0.06", "15": "0.07", "1": "0.01"},
  }
```

Scoring is done in a very naive way, by adding the distances in the 4 dimensions (4 bytes of ip)

> It's like having 4 lottery wheels with 0-255 on each, spinning the 4 and adding the scores. 

```
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
    return score
```

Again, this scoring is too naive as it does not keep the c-class information.
every digit of the ip has equal importance, and in the end all that counts is the quantity.



### linear_ip_lottery

See simulations/linear_ip_lottery/stats.json and related CSVs

```
{"Simulation": "linear_ip_lottery",
  "Total": 20000, "Consensus": 16535,
  "Consensus_PC": "82.67",
  "Queue": {"127": 64, "63": 28, "31": 45, "15": 17, "1": 6221},
  "Classes": {"127": 82, "63": 24, "31": 158, "15": 145, "1": 19591},
  "Classes_PC": {"127": "0.41", "63": "0.12", "31": "0.79", "15": "0.73", "1": "97.95"},
  "Classes_global_PC": {"127": "0.01", "63": "0.00", "31": "0.02", "15": "0.04", "1": "0.02"},
  }
```

Scoring:
First 4 bytes of the cycle_hash are converted to an integer.  
Verifier IP is converted to an integer as well, most significant byte first.  
That way, full IP space is mapped to a single dimension, with a.b.c.d.2 being equal to a.b.c.d.1 + 1  
full c-class remain grouped.  

> All possible ips are on the lottery wheel, sorted, from 0.0.0.0 to 255.255.255.255.   
> Some areas are more dense in eligible ips than others.  
> You spin the wheel and take the closest eligible ip.

This scoring requires less resources to compute than the regular scoring

```
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
    return score
```

At first glance, this may look fine.  IP from small classes have more odds than ip in large classes.   
It's not.

Consensus dropped. Why? Because the IP space is not uniform, and the queue IP space is even less uniform because, you know, large blocks on a small number of ISP (OVH, AMAZON...) often close together.  
So - to use a simple example - nodes files may have their first ip as 3.33.15.23 and last one as 218.240.13.55
since the hash is random, we will draw 0.x.x.x, 1.x.x.x., 2.x.x.x but also 219.x.x.x up to 255.x.x.x  
All these are valid ips, that are not in nyzo queue. And every time you draw one of these, the larger or smaller ip of the node file wins.

So with this model, some ips have a - significantly - greater chance to win. This is not acceptable.    
Even if this is a by-product of current queue concentration on a few providers (quantity, not diversity), this would lead to another kind of concentration, not on the cheapest ip provider, but on the lowest and highest ip blocks.

### shuffle_ip_lottery

Broken WIP

### linear_ip_lottery2

See simulations/linear_ip_lottery2/stats.json and related CSVs

```
{
  "Simulation": "linear_ip_lottery2",
  "Total": 20000, "Consensus": 19152,
  "Consensus_PC": "95.76",
  "Queue": {"127": 64, "63": 28, "31": 45, "15": 17, "1": 6221},
  "Classes": {"127": 150, "63": 116, "31": 265, "15": 154, "1": 19315},
  "Classes_PC": {"127": "0.75", "63": "0.58", "31": "1.32", "15": "0.77", "1": "96.58"},
  "Classes_global_PC": {"127": "0.01", "63": "0.02", "31": "0.03", "15": "0.05", "1": "0.02"}
}
```

Idea here is to fuzz the first 2 bytes of the ip address to avoid the edge issues of liner_ip_lottery, as well as non uniformity of available ipv4 space (like 10.0.0.0 being private).  
A permutation table is applied to the {0..255} space and is used to shuffle bytes 1 and 2 of the ip.  
That table is built in a deterministic pseudo radom way, from the cycle hash.  

This means that every 50 blocks, as the cycle hash changes, the permutation table changes and maps the ip space in a different way.  
Only the first 2 bytes are shuffled, so full class C ranges remain grouped.

The shuffle map only needs to be built once per 50 blocks.  
I used a python shuffle(), a Knuth shuffle with any prng can do.

```
def shuffle(cycle_hash: bytes):
    global SHUFFLE_MAP
    SHUFFLE_MAP = [i for i in range(256)]
    random = Random(cycle_hash)
    random.shuffle(SHUFFLE_MAP)
```

Scoring:

```
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
    hash_int = int.from_bytes(cycle_hash[:4], "big")
    score = abs(hash_int - ip_int)
    return score
```

> It's like you take the whole IP space ribbon (one dimension), cut it in 256x256 equal pieces (no C-class will be cut), shuffle them and glue them back on the lottery wheel.  
> Every 50 blocks, you shuffle in a different way and get a new layout.
> Then you spin the wheel and take the closest eligible ip.  
> Some regions are more dense than others, hence diversity is favored instead of quantity.  

- As seen in the stats, ips in classes smaller than 128 ips have more chances to win than the average ip in a 128+ ip class.  
- Consensus remains good, way better than the previous naive scoring.  
- all entropy from cycle_hash still is used, as seed for the permutation map.  
- computation requirements are light, lighter than current lottery scoring (no hash, no 2x32 additions)  
- permutation map is only to be done once per 50 blocks  
- since the permutation changes every 50 blocks, non uniformity in the queue ip address space is averaged over time, and you can't knwo what ip will have more chances in one month. This again encourages diversity.   

Some bias still exist.    
I believe ip in lower and higher range of B and C class may have a slight edge.    
This is harder to detect but I'll try to push the simulation further and see if I can model that.

Any help is welcome!
