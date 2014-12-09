from google.appengine.ext import ndb
import logging


# DB schema:
# Name, Surname, YearTo, House, Address1, Address2, Address3, Address4,
# City, State, Pincode, Country, Phone1R, Phone1W, Phone2W, Fax, Profession
# Email, Phone2R, Status

class Oldboy(ndb.Model):
	# Database properties

	# Basic info.
	firstname 	= ndb.StringProperty(indexed = True)
	surname 	= ndb.StringProperty(indexed = True)
	year 		= ndb.IntegerProperty(indexed = True)
	house 		= ndb.StringProperty()
	
	# Address info.
	address1 	= ndb.StringProperty()
	address2 	= ndb.StringProperty()
	address3 	= ndb.StringProperty()
	address4 	= ndb.StringProperty()
	city 	 	= ndb.StringProperty()
	state 	 	= ndb.StringProperty()
	pincode 	= ndb.StringProperty()
	country 	= ndb.StringProperty()
	
	# Phone info.
	phone1r 	= ndb.StringProperty()
	phone2r 	= ndb.StringProperty()
	phone1w 	= ndb.StringProperty()
	phone2w 	= ndb.StringProperty()
	fax 		= ndb.StringProperty()
	
	# Other info.
	profession 	= ndb.StringProperty()
	email 		= ndb.StringProperty()
	status 		= ndb.StringProperty()

	last_updated = ndb.DateTimeProperty(auto_now_add = True)


	# Read this
	# https://cloud.google.com/appengine/docs/python/ndb/queries

	# @classmethod
	# def add_entry():

	@classmethod
	def get_entry_by_year():



# new_entry = Oldboy(
# 			firstname = "Bob",
# 			surname = "Smith",
# 			year = 1973
# 	)
# new_entry.put()

# q = Oldboy.query()
# for qry in q.fetch():
# 	logging.info("%s" % str(qry))

qry = Oldboy.query()
logging.info("count  = %d" % qry.count())
for q in qry.filter(Oldboy.surname == "Son").fetch():
	logging.info("%s %s" % (str(q.firstname), str(q.surname)))


qry = Oldboy.query()
logging.info("count  = %d" % qry.count())
for q in qry.filter(Oldboy.year == 1989).fetch():
	logging.info("%s %s" % (str(q.firstname), str(q.surname)))



	# qry = Oldboy.query(Oldboy.year == <value here>)



