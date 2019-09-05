import csv
import sys

finalRows = []
files = sys.argv[1:-1]

for file in files:
  f = "./csv/out/"+file+".csv"
  reader = csv.DictReader(open(f))
  for row in reader:
    rowList = row.values()
    finalRows.append(rowList)


gluedFileName = sys.argv[-1]
file = "csv/out/"+gluedFileName+".csv"

with open(file, "wb") as f:
  writer = csv.writer(f)
  writer.writerow(["QB", "RB", "RB","WR","WR","WR","FLEX","S-FLEX"])
  writer.writerows(finalRows)