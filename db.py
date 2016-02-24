# Related DB info found here
# https://cloud.google.com/appengine/docs/python/ndb/queries

__author__ = 'rohitsm'
__page__ = 'https://github.com/rohitsm/spsoldboys'

# Google App Engine
from google.appengine.ext import ndb
import logging

# Python
import csv
import sys
from collections import OrderedDict

# Application related files
from cleanup import CleanUp
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
	year 		= ndb.StringProperty()
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

	
	# Class method that gets entries from datastore based on values of 'firstname', 'surname' and/or 'year'
	@classmethod
	def lookup_datastore(self, firstname, surname, year):

		# For debugging purposes
		# print "before DB query %s %s %s " % (firstname, surname, year)

		if firstname is not None:

			# Firstname + Year
			if year is not None:
				return Oldboy.query(ndb.AND(Oldboy.firstnameLC == firstname, Oldboy.year == year))  \
									.order(Oldboy.firstnameLC).order(Oldboy.year)
			# Firstname + Surname
			if surname is not None:
				return Oldboy.query(ndb.AND(Oldboy.firstnameLC == firstname, Oldboy.surnameLC == surname))  \
									.order(Oldboy.surnameLC).order(Oldboy.firstnameLC)

			# Firstname	
			return Oldboy.query(Oldboy.firstnameLC == firstname).order(Oldboy.firstnameLC)

		if surname is not None:
			
			# Surname + Year
			if year is not None:
				return Oldboy.query(ndb.AND(Oldboy.surnameLC == surname, Oldboy.year == year))  \
									.order(Oldboy.surnameLC).order(Oldboy.year)

			# Surname + Firstname
			if firstname is not None:
				return Oldboy.query(ndb.AND(Oldboy.surnameLC == surname, Oldboy.firstnameLC == firstname))  \
									.order(Oldboy.surnameLC).order(Oldboy.firstnameLC)

			# Surname
			return Oldboy.query(Oldboy.surnameLC == surname).order(Oldboy.surnameLC)
		
		# Year
		return Oldboy.query(Oldboy.year == year).order(Oldboy.year)


	# Return datastore record as a list of dict
	@classmethod
	def get_record(self, firstName, lastName, year ):
		
		# Lookup datastrore
		qry = Oldboy.lookup_datastore(firstName, lastName, year)
		
		if (qry.count() == 0):
			return None

		# print "inside get_record()"
	    
		# Format of each db record
		ob_entries = []

		for q in qry.fetch():

			ob_entry = OrderedDict()
			ob_entry['First Name']  = str(q.firstname)
			ob_entry['Last Name']   = str(q.surname)
			ob_entry['Year']        = str(q.year)
			ob_entry['House']       = str(q.house)

			# Address info
			ob_entry['Address 1']   = str(q.address1)
			ob_entry['Address 2']   = str(q.address2)
			ob_entry['Address 3']   = str(q.address3)
			ob_entry['Address 4']   = str(q.address4)
			ob_entry['City']        = str(q.city)
			ob_entry['State']       = str(q.state)
			ob_entry['Postal Code'] = str(q.pincode)
			ob_entry['Country']     = str(q.country)

			# Phone info.
			ob_entry['Phone 1 (R)'] = str(q.phone1r)
			ob_entry['Phone 2 (R)'] = str(q.phone2r)
			ob_entry['Phone 1 (W)'] = str(q.phone1w)
			ob_entry['Phone 2 (W)'] = str(q.phone2w)
			ob_entry['Fax']         = str(q.fax)

			# Other info.
			ob_entry['Profession']  = str(q.profession)
			ob_entry['Email']       = str(q.email)
			ob_entry['Status']      = str(q.status)

			ob_entry['Last Updated'] = str(q.last_updated)

			# print 'ob_entry = ', ob_entry
			ob_entries.append(ob_entry)

		return ob_entries


	# For adding entry into the datastore. Reads input from .csv file. 
	# Function called in index() in main.py. Function uses datastore schema mentioned above. 
	@classmethod
	def set_record(self):
		# record = Oldboy.query().get()
		# print "type = ", type(record)
		# print "Record = ", record

		# Reading from the csv files
		num_of_records_written = 0
		try:
			with open('relatedFiles/oldboys.csv', 'rU') as csvfile:
				entry_list = []
				reader = csv.reader(csvfile, delimiter = ',', quotechar = "|", dialect=csv.excel_tab)
				for row in reader:
					if num_of_records_written != 0: #Skip table headers
						entry_list = cleanup.remove_quotes(list(row))
						
						# Print out list of entries as they are being read from csv file
						# print  "entry_list = ", entry_list

						first_name = str(entry_list[0]).upper()
						last_name = str(entry_list[1]).upper()
						yr = str(cleanup.adjust_year(entry_list[2])).upper()

						# Lookup datastrore
						qry = Oldboy.get_record(firstName, lastName, year)
						
						if (qry is not None):
							# Record
							delete_from_db(first_name, last_name, year)

						
						oldboy_entry = Oldboy(
							firstname 	= first_name,
							surname 	= last_name,
							year 		= yr
							house 		= str(entry_list[3]).upper(),
							
							# Address info
							address1 	= str(entry_list[4]).upper(),
							address2 	= str(entry_list[5]).upper(),
							address3 	= str(entry_list[6]).upper(),
							address4 	= str(entry_list[7]).upper(),
							city 	 	= str(entry_list[-12]).upper(),
							state 	 	= str(entry_list[-11]).upper(),
							pincode 	= str(entry_list[-10]).upper(),
							country 	= str(entry_list[-9]).upper(),
							
							# Phone info.
							phone1r 	= str(entry_list[-8]).upper(),
							phone2r 	= str(entry_list[-7]).upper(),
							phone1w 	= str(entry_list[-6]).upper(),
							phone2w 	= str(entry_list[-5]).upper(),
							fax 		= str(entry_list[-4]).upper(),
							
							# Other info.
							profession 	= str(entry_list[-3]).upper(),
							email 		= str(entry_list[-2]).upper(),
							status 		= str(entry_list[-1]).upper(),
							
							# To enable lookups
							firstnameLC = str(cleanup.remove_punctuations(entry_list[0])).lower(),
							surnameLC 	= str(cleanup.remove_punctuations(entry_list[1])).lower()
							)
						oldboy_entry.put()
						
						# Print out list of entries as they are being written to the datastore.
						# print oldboy_entry
						
					print "num_of_records_written = ", num_of_records_written # Counter for number of records
					num_of_records_written+= 1

			# Close the file
			csvfile.close()
			return num_of_records_written
		except:
			logging.error(sys.exc_info())

	def delete_from_db():
		"""For deleting entries that already exist
		"""
			
