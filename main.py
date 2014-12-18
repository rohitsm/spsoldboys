"""`main` is the top level module for your Flask application."""

__author__ = 'rohitsm'
__page__ = 'https://github.com/rohitsm/spsoldboys'

# Python
import urllib2
import json
import sys
from collections import OrderedDict

# Flask
from flask import Flask
from flask import request, redirect, url_for
from flask import render_template

# App Engine
from google.appengine.ext import ndb
import logging

# Application related files
import config
from db import Oldboy

app = Flask(__name__, static_url_path='/static')

# URL = recaptcha_url? + secret=your_secret & response=response_string&remoteip=user_ip_address'
recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'

# ReCAPTCHA secret key
recaptcha_secret = config.conf['SHARED_KEY']

@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    # Oldboy.add_entry()
    return render_template('index.html')

def verify_captcha(recaptcha_response):
	res =  recaptcha_url + \
			"?secret=" + recaptcha_secret + \
			"&response=" + recaptcha_response

	# resp = True|False Type=bool
	resp = json.load(urllib2.urlopen(res))["success"]
	# print "resp[success] = %r" %resp
	return resp


@app.route('/search', methods=['GET', 'POST'])
def authentication():
    # Verify reCaptcha input and render page correctly if captcha verified
    if request.method == 'POST':
    	if(verify_captcha(request.form['g-recaptcha-response'])):
    		return render_template('search.html')
        # return render_template('search.html') #Delete this line and uncomment 2 above
    
    # For GET requests
    return redirect(url_for('index'))

# Read data from DB and convert it to a list of dict and return it
def get_search_record( qry ):
    print "inside get_search_record()"
    
    # Format of each db record
    total_ob_entries = []

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
        total_ob_entries.append(ob_entry)

    # print "Len of total_ob_entries = ", total_ob_entries
    return total_ob_entries, ob_entry

# Send data from DB to 'results' page
@app.route('/results', methods=['GET', 'POST'])
def search_request():
    # Get search terms
    record = []
    # For table headers in while rendering table in the results
    headers = {} 
    if request.method == 'POST':
        try:
            oldboy_fname = request.form['firstname'].lower()
            oldboy_lname = request.form['lastname'].lower()
            year = request.form['year']
            # print "oldboy_fname : %s" %oldboy_fname
            # print "oldboy_lname : %s" %type(oldboy_lname)
            # print "year : %s" % type(year)

            if(not year):
                print "year null"
                year = None
            
            if( (not oldboy_fname) or (oldboy_fname.isspace()) ):
                print "fname null"
                oldboy_fname = None

            if( (not oldboy_lname) or (oldboy_lname.isspace()) ):
                print "lname null"
                oldboy_lname = None

            print "YEAR = ", year
            qry = Oldboy.get_query(oldboy_fname, oldboy_lname, year)
            print "Count = ", qry.count()

            if (qry.count() != 0):
                record, headers = get_search_record(qry)

                # Records sorted by Last names
                rec = sorted(record, key=lambda k: k['Last Name'])

                # print "Dict = ", rec
                return render_template('results.html', records = rec, headers = headers, count = qry.count())

            return render_template('notfound.html')
        
        except:
            print "Woah horsey! This shouldn't be happening!"
            print sys.exc_info() 
            # Add redirect to incorrect page
            return render_template('notfound.html')

    # For GET requests
    return redirect(url_for('index'))

@app.route('/addrecord')
def addrecord():
    """ Return page with Google form embedded
        in it for entering new record."""
    
    return render_template('addrecord.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
