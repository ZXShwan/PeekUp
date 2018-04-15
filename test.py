# from pli import PLI
# import pandas as pd
import sys
import csv

# data = pd.read_csv(sys.argv[1])
line = csv.reader(sys.stdin)
s = set()
for entry in line:
    value = entry[0] + "," + entry[1] + "," + entry[2]
    if value in s:
        print("Non-unique")
        exit()
    s.add(value)

print("unique")
