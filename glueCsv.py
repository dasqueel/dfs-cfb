import csv

finalRows = []
files = ['yay', 'bob', 'cat','test']

for file in files:
  # print 'file: ', file
  f = "./csv/out/"+file+".csv"
  reader = csv.DictReader(open(f))
  for row in reader:
    # print row
    rowList = row.values()
    # print rowList
    finalRows.append(rowList)

print finalRows

gluedFileName = 'money'
file = "csv/out/"+gluedFileName+".csv"
with open(file, "wb") as f:
  writer = csv.writer(f)
  writer.writerow(["QB", "RB", "RB","WR","WR","WR","FLEX","S-FLEX"])
  writer.writerows(finalRows)