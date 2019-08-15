import csv
import random
import pprint
import flask
from flask import *

app = flask.Flask(__name__)
app.secret_key = "aaabbbbccc"
pp = pprint.PrettyPrinter(indent=4)
reader = csv.DictReader(open("./csv/cfb1.csv"))

@app.route("/")
def contest():
	players = {"qbs" : [], "rbs" : [], "wrs" : []}
	for row in reader:
		print(row)
		try:
			playerObj = {
				"name" : "",
				"id" : "",
				"pos" : "",
				"sal" : "",
				"date" : "",
				"team" : "",
			}
			row = row.values()
			player = row[2]
			# print player
			playerObj["name"] = player[1]
			playerObj["id"] = player[2]
			playerObj["pos"] = player[3][:2]
			playerObj["sal"] = int(player[4])
			playerObj["date"] = player[5]
			playerObj["team"] = player[6]

			if playerObj["pos"] == "QB": players["qbs"].append(playerObj)
			if playerObj["pos"] == "RB": players["rbs"].append(playerObj)
			if playerObj["pos"] == "WR": players["wrs"].append(playerObj)

		except:
			# print 'error: '
			pass

	return jsonify(players)

# take in json from react app
# @app.route("/out",methods=["POST"])
# def out():
# 	json = request.get_json()
# 	print json

# 	qbs = json["qbs"]
# 	rbs = json["rbs"]
# 	wrs = json["wrs"]

# 	lineups = flexNormalizer(setLineups(qbs, rbs, wrs))

# 	idLineups = []
# 	for lineup in lineups:
# 		l = [
# 			lineup["qb"]["id"],
# 			lineup["rb1"]["id"],
# 			lineup["rb2"]["id"],
# 			lineup["wr1"]["id"],
# 			lineup["wr2"]["id"],
# 			lineup["wr3"]["id"],
# 			lineup["flex"]["id"],
# 			lineup["sflex"]["id"]
# 		]
# 		idLineups.append(l)
# 	for l in lineups: pp.pprint(l)

# 	with open("csv/dkout.csv", "wb") as f:
# 			writer = csv.writer(f)
# 			writer.writerow(["QB", "RB", "RB","WR","WR","WR","FLEX","S-FLEX"])
# 			writer.writerows(idLineups)

# 	return "ok"

if __name__ == "__main__":
    # app.run(debug = True, host="127.0.0.1", port=5001)
    app.run(debug = True, use_reloader=True)