import csv
import random
import flask
import traceback
import sys
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.secret_key = "aaabbbbccc"

@app.route("/<contestType>/<csvFile>")
def contest(contestType, csvFile):
	if contestType == 'classic':
		f = "./csv/"+csvFile+".csv"
		reader = csv.DictReader(open(f))
		players = {"qbs" : [], "rbs" : [], "wrs" : []}

		for row in reader:
			try:
				playerObj = {
					"name" : "",
					"id" : "",
					"pos" : "",
					"sal" : "",
					"date" : "",
					"team" : "",
				}
				rowList = row.values()

				player = None
				for el in rowList:
					# the first instance of a list isnt always a player list
					if type(el) == list:
						if el[0] != 'Name + ID':
							player = el

				if player != None:
					playerObj["name"] = player[1]
					playerObj["id"] = player[2]
					playerObj["pos"] = player[3][:2]
					playerObj["sal"] = int(player[4])
					playerObj["date"] = player[5]
					playerObj["team"] = player[6]

					if playerObj["pos"] == "QB": players["qbs"].append(playerObj)
					if playerObj["pos"] == "RB": players["rbs"].append(playerObj)
					if playerObj["pos"] == "WR": players["wrs"].append(playerObj)

			except Exception as e:
				traceback.print_exc(file=sys.stdout)
				print e

		return flask.jsonify(players)

	elif contestType == 'showdown':
		f = "./csv/"+csvFile+".csv"
		reader = csv.DictReader(open(f))
		players = {"captains": [], "utilities": []}

		for row in reader:
			try:
				playerObj = {
					"name" : "",
					"id" : "",
					"pos" : "",
					"sal" : "",
					"date" : "",
					"team" : "",
				}
				rowList = row.values()
				# print rowList

				player = None
				for el in rowList:
					# the first instance of a list isnt always a player list
					if type(el) == list:
						if el[0] != 'Name + ID':
							player = el

				# print player

				if player != None:
					playerObj["name"] = player[1]
					playerObj["id"] = player[2]
					playerObj["pos"] = player[3][:2]
					playerObj["sal"] = int(player[4])
					playerObj["date"] = player[5]
					playerObj["team"] = player[6]

					if playerObj["pos"] == "CP": players["captains"].append(playerObj)
					if playerObj["pos"] == "UT": players["utilities"].append(playerObj)

				# print playerObj

			except Exception as e:
				print e

		# print players
		return flask.jsonify(players)
		# return 'would return showdown url'

	else:
		return 'https://reddit.com/r/cfb/new'

@app.route("/test")
def test():
	return 'aaayyeeee :D'

# take in json from react app
@app.route("/out",methods=["POST"])
def out():
	json = flask.request.get_json()

	qbs = json["finalQbs"]
	# rbs = json["finalRbs"]
	rbs = sorted(json["finalRbs"], key = lambda i: i['shares'], reverse=True)
	# wrs = json["finalWrs"]
	wrs = sorted(json["finalWrs"], key = lambda i: i['shares'], reverse=True)

	# print 'rbs', rbs
	# print 'wrs', wrs

	totalEnteries = json["totalEnteries"]
	fileName = json["fileName"]

	lineups = [['' for x in range(0,8)] for i in range(0,totalEnteries)]

	'''
		if doing the create lineups on a list of 3k players
	'''

	qb1 = qbs[0]
	for i in range(0,qb1["shares"]):
		lineups[i][0] = str(qb1["id"])

	qb2 = qbs[1]
	for i in range(0,qb2["shares"]):
		lineups[i][7] = str(qb2["id"])

	rb1 = rbs[0]
	for i in range(0,rb1["shares"]):
		lineups[i][1] = str(rb1["id"])

	rb2 = rbs[1]
	for i in range(0,rb2["shares"]):
		lineups[i][2] = str(rb2["id"])

	wr1 = wrs[0]
	for i in range(0,wr1["shares"]):
		lineups[i][3] = str(wr1["id"])

	wr2 = wrs[1]
	for i in range(0,wr2["shares"]):
		lineups[i][4] = str(wr2["id"])

	# wr3 = wrs[2]
	# for i in range(0,wr3["shares"]):
	# 	lineups[i][5] = str(wr3["id"])

	# need to sort the wrs or rbs by shares
	if len(rbs) > 2 and rbs[2]['shares'] > 1:
		# flex is filled with rbs
		# we are varying on wr3
		# want to loop over all wr2 and beyond
		# how do we know vary on wr3?
		for i, wr in enumerate(wrs[2:]):
			# pass
			# print 'would add: ',i ,wr['name'], wr['id']
			lineups[i][5] = str(wr['id'])
	else:
		wr3 = wrs[2]
		for i in range(0,wr3["shares"]):
			lineups[i][5] = str(wr3["id"])

	# handle flex
	# need to update when varying on wr3
	# print 'totalenteries', totalEnteries
	# print 'len rbs', len(rbs)
	if len(rbs) == 3:
		# pass
		rb3 = rbs[2]
		for i in range(0,rb3["shares"]):
			lineups[i][6] = str(rb3["id"])
	else:
		flexSpot = 0
		if len(rbs) > totalEnteries:
			for i in range(2, len(rbs)):
				rb = rbs[i]
				# print 'flex rb:', rb['name']
				lineups[flexSpot][6] = str(rb["id"])
				flexSpot += 1

		if len(wrs) > totalEnteries:
			for i in range(3, len(wrs)):
				wr = wrs[i]
				lineups[flexSpot][6] = str(wr["id"])
				# lineups[i - 3][6] = wr["name"]
				flexSpot += 1

	for l in lineups: print l

	file = "csv/out/"+fileName+".csv"
	with open(file, "wb") as f:
		writer = csv.writer(f)
		writer.writerow(["QB", "RB", "RB","WR","WR","WR","FLEX","S-FLEX"])
		writer.writerows(lineups)

	return 'https://dfs-cfb.herokuapp.com/csv/'+fileName
	# return 'http://localhost:5000/csv/'+fileName

	# lineups = flexNormalizer(setLineups(qbs, rbs, wrs))

@app.route('/csv/<fileName>') # this is a job for GET, not POST
def plot_csv(fileName):
		file = 'csv/out/'+fileName+'.csv'
		fileAttach = fileName+'.csv'
		return flask.send_file(file, mimetype='text/csv', attachment_filename=fileAttach, as_attachment=True)

if __name__ == "__main__":
		# app.run(debug = True, host="127.0.0.1", port=5001)
		app.run(debug = True, use_reloader=True)