# Related DB info found here
# https://cloud.google.com/appengine/docs/python/ndb/queries

# Google App Engine
from google.appengine.ext import ndb
import logging

# Python
import csv
import string

# Application related files
from cleanup import CleanUp


# def remove_punctuations(word):
# 	exclude = set(string.punctuation)
# 	word = ''.join(ch for ch in word if ch not in exclude)
# 	return word

cleanup = CleanUp()

# DB schema:
# Name, Surname, YearTo, House, Address1, Address2, Address3, Address4,
# City, State, Pincode, Country, Phone1R, Phone2R, Phone1W, Phone2W, Fax, 
# Profession, Email, Status

class Oldboy(ndb.Model):
	# Database properties

	# Basic info.
	firstname 	= ndb.StringProperty()
	surname 	= ndb.StringProperty()
	year 		= ndb.IntegerProperty()
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

	# Query related info.
	last_updated = ndb.DateTimeProperty(auto_now_add = True)
	firstnameLC = ndb.StringProperty()		# firstname in lowercase
	surnameLC 	= ndb.StringProperty()		# lastname in lowercase

	@classmethod
	def get_query(self, firstname, surname, year):
		
		print "before DB query %s %s %s " % (firstname, surname, year)

		if firstname is not None:

			# Firstname + Year
			if year != 0:
				print "1 %s %s %s " % (firstname, surname, year)
				return Oldboy.query(ndb.AND(Oldboy.firstnameLC == firstname, Oldboy.year == year))  \
									.order(Oldboy.firstnameLC).order(Oldboy.year)
			# Firstname + Surname
			if surname is not None:
				print "2 %s %s %s " % (firstname, surname, year)
				return Oldboy.query(ndb.AND(Oldboy.firstnameLC == firstname, Oldboy.surnameLC == surname))  \
									.order(Oldboy.surnameLC).order(Oldboy.firstnameLC)

			# Firstname
			print "3 %s %s %s " % (firstname, surname, year)
			return Oldboy.query(Oldboy.firstnameLC == firstname).order(Oldboy.firstnameLC)

		if surname is not None:
			
			# Surname + Year
			if year != 0:
				print "4 %s %s %s " % (firstname, surname, year)
				return Oldboy.query(ndb.AND(Oldboy.surnameLC == surname, Oldboy.year == year))  \
									.order(Oldboy.surnameLC).order(Oldboy.year)

			# Surname + Firstname
			if firstname is not None:
				print "5 %s %s %s " % (firstname, surname, year)
				return Oldboy.query(ndb.AND(Oldboy.surnameLC == surname, Oldboy.firstnameLC == firstname))  \
									.order(Oldboy.surnameLC).order(Oldboy.firstnameLC)

			# Surname
			print "6 %s %s %s " % (firstname, surname, year)
			return Oldboy.query(Oldboy.surnameLC == surname).order(Oldboy.surnameLC)

		
		# Year
		print "after DB query %s %s %s " % (firstname, surname, year)
		return Oldboy.query(Oldboy.year == year).order(Oldboy.year)

	@classmethod
	def add_entry(self):
		record = Oldboy.query().get()
		print "type = ", type(record)
		print "Record = ", record

		# Reading from the csv files
		with open('relatedFiles/oldboys.csv', 'rU') as csvfile:
			entry_list = []
			reader = csv.reader(csvfile, dialect=csv.excel_tab)	
			i = 0
			for row in reader:
				if i != 0:
					entry_list = list(row[0].split(','))	#row is of 'List' type
					print  "entry_list = ", entry_list
					oldboy_entry = Oldboy(
						firstname 	= str(entry_list[0]),
						surname 	= str(entry_list[1]),
						year 		= int(entry_list[2]),
						house 		= str(entry_list[3]),
						
						# Address info
						address1 	= str(entry_list[4]),
						address2 	= str(entry_list[5]),
						address3 	= str(entry_list[6]),
						address4 	= str(entry_list[7]),
						city 	 	= str(entry_list[8]),
						state 	 	= str(entry_list[9]),
						pincode 	= str(entry_list[10]),
						country 	= str(entry_list[11]),
						
						# Phone info.
						phone1r 	= str(entry_list[12]),
						phone2r 	= str(entry_list[13]),
						phone1w 	= str(entry_list[14]),
						phone2w 	= str(entry_list[15]),
						fax 		= str(entry_list[16]),
						
						# Other info.
						profession 	= str(entry_list[17]),
						email 		= str(entry_list[18]),
						status 		= str(entry_list[19]),
						
						firstnameLC = cleanup.remove_punctuations(entry_list[0]).lower(),
						surnameLC 	= cleanup.remove_punctuations(entry_list[1]).lower()
						)
					oldboy_entry.put()

					break
				i+= 1


		





# new_entry = Oldboy(
# 			firstname = "Bob",
# 			surname = "Smith",
# 			year = 1973
# 	)
# new_entry.put()

# q = Oldboy.query()
# for qry in q.fetch():
# 	logging.info("%s" % str(qry))

# qry = Oldboy.query(Oldboy.surnameLC == "Smith").order(-Oldboy.firstnameLC).order(Oldboy.year)
# logging.info("count  = %d" % qry.count())
# for q in qry.fetch():
# 	logging.info("%s %s %s" % (str(q.firstnameLC), str(q.surnameLC), str(q.year)))

# qry = Oldboy.query(ndb.AND(Oldboy.surnameLC == "Smith", Oldboy.year == 1973)).order(Oldboy.firstnameLC).order(Oldboy.year)
# logging.info("count  = %d" % qry.count())
# for q in qry.fetch():
# 	logging.info("%s %s %s" % (str(q.firstnameLC), str(q.surnameLC), str(q.year)))



# qry = Oldboy.query(Oldboy.year == 1973)
# logging.info("count  = %d" % qry.count())
# for q in qry.fetch():
# 	logging.info("%s %s" % (str(q.firstnameLC), str(q.surnameLC)))



	# qry = Oldboy.query(Oldboy.year == <value here>)



