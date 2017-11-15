'''
	Author : nitin.jamadagni@gmail.com
	precursors : Flask
	Usage : python core.py OPT <host> <port>
			OPT : SETUP/RUN
'''


'''
Imports section
'''
from flask import Flask, jsonify, request
import sys
from pymongo import MongoClient


'''
Setup and globals
'''
if len(sys.argv) is not 4:
	print "Usage : python core.py OPT <host> <port>\n OPT : SETUP/RUN"
app = Flask("authentication_service")
client = MongoClient('localhost' , 27017)
db = client["usermetadata"]





'''
Utility functions
'''
def setupandexit():
	db.create_collection("authentication")
	db["authentication"].create_index([('username',pymongo.ASCENDING)],unique=True)



'''
Main Functionalities
'''
@app.route('/')
def default():
	response = {"status" : "success",\
				"response" : "Use the following  model for service\n \
				1. /register/<username> [response of a token] \n\
				2. /authenticate/<username> [response of a authentication accept] \n\
				3. /refreshtoken/<username> [renew token and send back new]\n\
				"}
	return jsonify(response)

@app.route('/authenticate/<string:username>')
def authenticate(username):
	response = {}
	userprofile = db["authentication"].find_one(filter={"username" : username}, projection={'_id':False,'key':True, 'username' : True , 'validtill' : True})
	if username.count() == 0:
		response["status"] = "fail"
		response["response"] = "User not registered yet"
		return jsonify(response)

	# NITIN : NOTE : Check for expiry of token later

	if request.args.key == str(userprofile["key"]):
		response["status"] = "success"
		response["response"] = {"username" : userprofile["username"] , "Authenticated" : True}
		return jsonify(response)
	else:
		response["status"] = "success"
		response["response"] = {"username" : userprofile["username"] , "Authenticated" : False}
		return jsonify(response)
	 



'''
Program Flow
'''
if __name__ == '__main__':
	if sys.argv[1] == "RUN":
		app.run(host = sys.argv[2],port = sys.argv[3],debug = True)
	elif sys.argv[1] == "SETUP":
		setupandexit()