3,200,000 lottery events, from the same nodes files

Built from simu11b.py  
`cat all.csv | sort | uniq -c > all.count.csv`

sort  
`cat all.count.csv | sort -g -r | more`  
`cat all.count.csv | sort -g -r > all.count.sorted.csv`

Extract c-classes, count and sort
`cat all.csv |cut -d',' -f 2 | sort | uniq -c | sort -g -r > allc.count.sorted.csv`
