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
	def get_query(self, firstname=None, surname=None, year=None):

		if surname is not None:
			
			# Surname + Firstname
			if firstname is not None:
				return Oldboy.query(ndb.AND(Oldboy.surname == surname, Oldboy.firstname == firstname))  \
									.order(Oldboy.surname).order(Oldboy.firstname)

			# Surname + Year
			if year is not None:
				return Oldboy.query(ndb.AND(Oldboy.surname == surname, Oldboy.year == year))  \
									.order(Oldboy.surname).order(Oldboy.surname)

			# Surname
			return Oldboy.query(Oldboy.surname == surname).order(Oldboy.surname)

		if firstname is not None:

			# Firstname + year
			if year is not None:
				return Oldboy.query(ndb.AND(Oldboy.firstname == firstname, Oldboy.year == year))  \
									.order(Oldboy.firstname).order(Oldboy.year)

		# Year
		return Oldboy.query(Oldboy.year == year).order(Oldboy.year)

	@classmethod
	def get_query



# new_entry = Oldboy(
# 			firstname = "Bob",
# 			surname = "Smith",
# 			year = 1973
# 	)
# new_entry.put()

# q = Oldboy.query()
# for qry in q.fetch():
# 	logging.info("%s" % str(qry))

# qry = Oldboy.query(Oldboy.surname == "Smith").order(-Oldboy.firstname).order(Oldboy.year)
# logging.info("count  = %d" % qry.count())
# for q in qry.fetch():
# 	logging.info("%s %s %s" % (str(q.firstname), str(q.surname), str(q.year)))

qry = Oldboy.query(ndb.AND(Oldboy.surname == "Smith", Oldboy.year == 1973)).order(Oldboy.firstname).order(Oldboy.year)
logging.info("count  = %d" % qry.count())
for q in qry.fetch():
	logging.info("%s %s %s" % (str(q.firstname), str(q.surname), str(q.year)))



# qry = Oldboy.query(Oldboy.year == 1973)
# logging.info("count  = %d" % qry.count())
# for q in qry.fetch():
# 	logging.info("%s %s" % (str(q.firstname), str(q.surname)))



	# qry = Oldboy.query(Oldboy.year == <value here>)



