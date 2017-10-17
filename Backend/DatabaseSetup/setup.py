import os
from Errors import exceptions as e
from pymongo import MongoClient

class DBMaintainance:
	def setup(self, configFile):
		self.configurations = None
		if os.path.exists(configFile):
			with open(configFile) as cfile:
				self.configurations = json.load(cfile)
		try :
			if self.configurations is None:
				self.client = MongoClient()
			else:
				self.client = MongoClient(self.configurations['host_ip'], self.configurations['port'])
		except:
			raise e.SimpleException('problem connecting to the db instance, try firing again!')



	def createOrUpdateDB(self, domainModelName):
		# NITIN : TODO : implement the authentications, user management etc later
		# NITIN : NOTE : if domain model DNE create a database for it

		# NITIN : TODO : check if it can be updated in place without loosing data
		if domainModelName in map(lambda a : str(a), self.client.database_names()):
			self.client.drop_database(domainModelName)
			
		# NITIN : TODO : call the collections creations services here, the database is created when collections are created			


	def getConnectionObject(self, domainModelName):
		if domainModelName not in map(lambda a: str(a), self.client.database_names()):
			return None
		return self.client.get_database(domainModelName)


	def shutdown(self):
		self.client.close()
