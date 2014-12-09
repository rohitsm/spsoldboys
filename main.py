"""`main` is the top level module for your Flask application."""
# Python
import urllib2
import json

# Flask
from flask import Flask
from flask import request, redirect, url_for
from flask import render_template

# Application related files
import config
from db import Oldboy

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
    	if(verify_captcha(request.form['g-recaptcha-response'])):
    		return render_template('search.html')
    
    return redirect(url_for('index'))


@app.route('/results', methods=['GET', 'POST'])
def search_request():
    # Get search terms
    if request.method == 'POST':
        oldboy_fname = request.form['firstname']
        oldboy_lname = request.form['lastname']
        year = request.form['year']
        print "oldboy_fname : %s" %oldboy_fname
        print "oldboy_lname : %s" %oldboy_lname
        print "year : %s" %year

        Oldboy.get_query(oldboy_fname, oldboy_lname, year)

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
