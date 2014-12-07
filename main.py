"""`main` is the top level module for your Flask application."""
# Python
import urllib2
import json

# Flask
from flask import Flask
from flask import request, redirect, url_for
from flask import render_template

# Load config file
import config

app = Flask(__name__)

# URL = recaptcha_url? + secret=your_secret & response=response_string&remoteip=user_ip_address'
recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
# ReCAPTCHA secret key
recaptcha_secret = config.conf['SHARED_KEY']

@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

def verify_captcha(recaptcha_response):
	res =  recaptcha_url + \
			"?secret=" + recaptcha_secret + \
			"&response=" + recaptcha_response

	# resp = True|False Type=bool
	resp = json.load(urllib2.urlopen(res))["success"]
	# print "resp[success] = %r" %resp
	return resp


@app.route('/auth', methods=['GET', 'POST'])
def authentication():
    # Verify reCaptcha input and render page correctly if captcha verified
    if request.method == 'POST':
    	if(verify_captcha(request.form['g-recaptcha-response'])):
    		return render_template('auth.html')
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
