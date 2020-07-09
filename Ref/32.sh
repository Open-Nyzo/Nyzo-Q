#!/bin/bash

# Simple sample script to start 32 simulations in background.

for i in {1..32}
do
   python3 simu10b.py > "mass$i.csv" &
done
