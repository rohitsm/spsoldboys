from google.appengine.ext import ndb


# DB schema:
# Name, Surname, YearTo, House, Edited, Address1, Address2, Address3, Address4,
# City, mailing, State, Pincode, Country, Phone1R, Phone1W, Phone2W, Fax, Profession
# Email, Phone2R, Status

class Oldboy(ndb.model):
	firstname = ndb.StringProperty(repeated = True)
	surname = ndb.StringProperty(repeated = True)
	year = ndb.IntegerProperty(repeated = True)
	house = ndb.StringProperty()
	# edited = ndb.DateProperty()
	address1 = ndb.StringProperty()
	address2 = ndb.StringProperty()
	address3 = ndb.StringProperty()
	address4 = ndb.StringProperty()
	city = ndb.StringProperty()
	mailing = ndb.StringProperty()
	state = ndb.StringProperty()
	pincode = ndb.StringProperty()
	country = ndb.StringProperty()
	phone1r = ndb.StringProperty()
	phone2r = ndb.StringProperty()
	phone1w = ndb.StringProperty()
	phone2w = ndb.StringProperty()
	fax = ndb.StringProperty()
	profession = ndb.StringProperty()
	email = ndb.StringProperty()
	status = ndb.StringProperty()



