"""
Simple check for ensuring shuffle uniformity (ok)
"""

"""
python3 test_nuiform.py > ABC.csv
cat ABC.csv | sort | uniq -c > ABC.count.csv
cat ABC.count.csv | sort -g -r > ABC.count.sorted.csv
"""

import sys
sys.path.append("../libs/")
from utils import random_hash, shuffle_plus

for test in range(100000):
    cycle_hash = random_hash()
    shuffle_plus(cycle_hash, display=True)
