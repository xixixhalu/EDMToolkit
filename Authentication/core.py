'''
	Author : nitin.jamadagni@gmail.com
	precursors : Flask
	Usage : python core.py OPT <host> <port>
			OPT : SETUP/RUN
			<host> : host to run this service on
			<port> : port to run this service on
'''


'''
Imports section
'''
from flask import Flask, jsonify, request
import sys
import pymongo
import uuid
import datetime as dt
import random


'''
Setup and globals
'''
if len(sys.argv) is not 4:
	print "Usage : python core.py OPT <host> <port>\n OPT : SETUP/RUN"
	exit(0)
app = Flask("authentication_service")
# NITIN : TODO : Please switch to appropriate mongo port when using
client = pymongo.MongoClient('localhost' , 32768)
db = client["usermetadata"]
# Please change the storage directory for user histopry file uploads
storagedir = "/Users/nitin/Documents/Academics/USC/UnpaidIntern/CodeBase/EDMToolkit/Authentication/Storage"





'''
Utility functions
'''
def setupandexit():
	'''
		db : usermetadata
			collection : authentication :
										{
											username :
											key :
											validtill :
										}
			collection : history : 
										{
											username : 
											uploads : 
													{
														domainModelName : 	[ 
																				{	
																					file : 
																			 		date : 
																				}
																			]
													}
										}
	'''
	db.create_collection("authentication")
	db["authentication"].create_index([('username',pymongo.ASCENDING)],unique=True)
	db.create_collection("history")
	db["history"].create_index([('username',pymongo.ASCENDING)],unique=True)

def create_random_key():
	return str(uuid.uuid4())

def create_expiry_object():
	return dt.datetime.now() + dt.timedelta(days = 30)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))





'''
Main Functionalities
'''
# NITIN : NOTE : assuming the user has same token for all his domain models, change later for an exclusive token for each domain model
@app.route('/')
def default():
	response = {"status" : "success", "response" : "Use the following  model for service 1. /register/<username> [] [response of a token] 2. /authenticate/<username> [send 'key' : key_value in header] [response of a authentication accept] 3. /refreshtoken/<username> [send 'key' : key_value in header] [renew token and send back new] 4. /registerUpload/<string:username>/<string:dmName> [send 'modelfile' : file] [get acknoledgement back]"}
	return jsonify(response)

@app.route('/authenticate/<string:username>')
def authenticate(username):
	response = {}

	if 'key' not in request.args:
		response["status"] = "fail"
		response["response"] = "'key' not sent in header"
		return jsonify(response)


	userprofile = db["authentication"].find_one(filter={"username" : username}, projection={'key':True, 'username' : True , 'validtill' : True})
	if userprofile is None:
		response["status"] = "fail"
		response["response"] = "User not registered yet"
		return jsonify(response)

	

	if request.args["key"] == str(userprofile["key"]):
		delta = userprofile["validtill"] - dt.datetime.now()
		if not delta >= dt.timedelta():
			print delta
			response["status"] = "fail"
			response["response"] = "try refreshing your token, it is expired"
			return jsonify(response)
		response["status"] = "success"
		response["response"] = {"username" : userprofile["username"] , "Authenticated" : True}
		return jsonify(response)
	else:
		response["status"] = "fail"
		response["response"] = {"username" : userprofile["username"] , "Authenticated" : False}
		return jsonify(response)


@app.route('/register/<string:username>')
def registerUser(username):
	response = {}
	userprofile = db["authentication"].find_one(filter={"username" : username} , projection = {'key' : False , 'username' : False , 'validtill' : False})
	if userprofile is not None:
		response["status"] = "fail"
		response["response"] = "User already registered"
		return jsonify(response)

	key = create_random_key()
	validtill = create_expiry_object()
	userprofile = { "username" : username , "key" : key , "validtill" : validtill}
	db["authentication"].insert_one({ "username" : username , "key" : key , "validtill" : validtill})
	db["history"].insert_one( {"username" : username , "uploads" : [] } ) 
	response["status"] = "success"
	response["response"] = {"message" : "Successfully registerd user, check the object in 'returnvalue' to get the key" , "returnvalue" : userprofile}
	return jsonify(response)


@app.route('/refreshtoken/<string:username>')
def refreshtoken(username):
	response = {}
	
	if 'key' not in request.args:
		response["status"] = "fail"
		response["response"] = "'key' not sent in header"
		return jsonify(response)

	userprofile = db["authentication"].find_one(filter={"username" : username}, projection={'key':True, 'username' : True , 'validtill' : True})
	if userprofile is None:
		response["status"] = "fail"
		response["response"] = "User not registered yet"
		return jsonify(response)

	if request.args["key"] == str(userprofile["key"]):
		key = create_random_key()
		validtill = create_expiry_object()
		db["authentication"].update_one(filter = {"username"  : username} , update = { '$set' : {'key' : key , 'validtill' : validtill} }, upsert = False)
		userprofile = { "username" : username , "key" : key , "validtill" : validtill}
		response["status"] = "success"
		response["response"] = {"message" : "Successfully updated key, check the object in 'returnvalue' to get the key" , "returnvalue" : userprofile}
		return jsonify(response)
	else:
		response["status"] = "fail"
		response["response"] = "wrong old key, provide correct old key to refresh token"
		return jsonify(response)

# NITIN : Send file in POST with dmfile:<file> as key-value pair	
@app.route('/registerUpload/<string:username>/<string:dmName>' , methods = ['POST'])
def upload(username, dmName):
	# NITIN : NOTE : the file is actually stored on simple file system with a special name
	# This is enough soliution instead of using the gridFs on mongo, as wer are not expecting 
	# a lot of files to be stored
	
	#NITIN : TODO : Add checks for the existance file in POST request

	userprofile = db["history"].find_one(filter={"username" : username} , projection = {"uploads" : False, "_id" : False})
	if userprofile is None:
		response["status"] = "fail"
		response["response"] = "User account DNE"
		return jsonify(response)

	tempQueryFileName =  randomword(10)
	db["history"].update_one(filter = {"username" : username} , update = {'$push' : { "dmName" : { "filename" : tempQueryFileName , "date" : dt.datetime.now()} }} , upsert = True)

	
	f = request.files['queryfile']
	f.save(storagedir + tempQueryFileName)

	response["status"] = "success"
	response["response"] = {"message" : "Successfully uploaded file"}
	return jsonify(response)



'''
Program Flow
'''
if __name__ == '__main__':
	if sys.argv[1] == "RUN":
		app.run(host = sys.argv[2],port = int(sys.argv[3]),debug = True)
	elif sys.argv[1] == "SETUP":
		setupandexit()