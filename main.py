"""`main` is the top level module for your Flask application."""

__author__ = 'rohitsm'
__page__ = 'https://github.com/rohitsm/spsoldboys'

# Python
import urllib2
import json
import sys
import cgi

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

# URL format: recaptcha_url? + secret=your_secret & response=response_string&remoteip=user_ip_address'
recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'

# ReCAPTCHA secret key
recaptcha_secret = config.conf['SHARED_KEY']

def verify_captcha(recaptcha_response):
    res =  recaptcha_url + \
            "?secret=" + recaptcha_secret + \
            "&response=" + recaptcha_response

    # resp = True|False Type=bool
    resp = json.load(urllib2.urlopen(res))["success"]
    # print "resp[success] = %r" %resp
    return resp


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    
    # To add entry to DB, uncomment below line. set_record() reads from csv input. 
    # num_of_records = Oldboy.set_record()
    # print "No of records written = " + str(num_of_records)
    # return "helloWorld!"
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def authentication():
    # Verify reCaptcha input and render page correctly if captcha verified
    if request.method == 'POST':
    	if(verify_captcha(request.form['g-recaptcha-response'])):
    		return render_template('search.html')
        return render_template('search.html') #Delete this line and uncomment 2 above
    
    # For GET requests
    return redirect(url_for('index'))


# Send data from DB to 'results' page
@app.route('/results', methods=['GET', 'POST'])
def search_request():
    
    # Get search terms
    record = []
    
    # For table headers of HTML tables
    headers = {} 
    if request.method == 'POST':
        try:
            firstName = cgi.escape(request.form['firstname'], True).lower().replace(' ', '')
            lastName = cgi.escape(request.form['lastname'], True).lower().replace(' ', '')
            year = cgi.escape(request.form['year'], True)
            # print 'firstname = %s \nlastName = %s, \nyear =%s ' %(firstName, lastName, year)

            if(not year):            
                year = None
            
            if( (not firstName) or (firstName.isspace()) ):
                firstName = None

            if( (not lastName) or (lastName.isspace()) ):
                lastName = None

            # Retrieve query from the datastore.
            # record = DB query results
            # header = for rendering table headers
            record = Oldboy.get_record(firstName, lastName, year) 
            # print "record = %s" %(record)

            if (record is not None):
                count = len(record)
                headers = record[0]

                # Records sorted by Last names
                sorted_records = sorted(record, key=lambda k: k['Last Name'])

                # print "Dict = ", sorted_records
                return render_template('results.html',  records = sorted_records, \
                                                        headers = headers, \
                                                        count = count)

            return render_template('notfound.html')
        
        except Exception as e:
            print "Woah horsey! This shouldn't be happening!"
            logging.error(sys.exc_info())
            print e

            # Redirect to "not_found" page
            return render_template('notfound.html')

    # For GET requests
    return redirect(url_for('index'))


@app.route('/addrecord')
def addrecord():
    """ Page contains Google form embedded for entering new record."""    
    return render_template('addrecord.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
