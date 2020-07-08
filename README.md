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

## Simulations

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
