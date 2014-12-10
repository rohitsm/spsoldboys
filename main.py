"""`main` is the top level module for your Flask application."""
# Python
import urllib2
import json
import sys

# Flask
from flask import Flask
from flask import request, redirect, url_for
from flask import render_template

# Application related files
import config
from db import Oldboy

# App Engine
from google.appengine.ext import ndb
import logging

app = Flask(__name__)

# URL = recaptcha_url? + secret=your_secret & response=response_string&remoteip=user_ip_address'
recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
# ReCAPTCHA secret key
recaptcha_secret = config.conf['SHARED_KEY']


# def add_to_db():
#     new_entry = Oldboy(
#                 firstname = 'John',
#                 surname = 'Smith',
#                 year = 1973,
#                 firstnameLC = 'John'.lower(),
#                 surnameLC = 'Smith'.lower()
#                 )
#     new_entry.put()

@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    # add_to_db()
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
    	# if(verify_captcha(request.form['g-recaptcha-response'])):
    	# 	return render_template('search.html')
        return render_template('search.html') #Delete this line and uncomment 2 above
    
    return redirect(url_for('index'))


@app.route('/results', methods=['GET', 'POST'])
def search_request():
    # Get search terms
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
                year = 0
            
            if( (not oldboy_fname) or (oldboy_fname.isspace()) ):
                print "fname null"
                oldboy_fname = None

            if( (not oldboy_lname) or (oldboy_lname.isspace()) ):
                print "lname null"
                oldboy_lname = None

            print "YEAR = ", year
            qry = Oldboy.get_query(oldboy_fname, oldboy_lname, int(year))
            print "Count = ", qry.count()

            if (qry.count() != 0):
                for q in qry.fetch():
                    logging.info("%s %s %s" % (str(q.firstname), str(q.surname), str(q.year)))
                return render_template('results.html')
        
        except:
            print "Woah horsey! This shouldn't be happening!"
            print sys.exc_info() 
            # Add redirect to incorrect page

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
