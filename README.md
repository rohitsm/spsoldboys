#### The Alumni Database of [St. Peter's School, Panchgani](st.peterspanchgani.org) ####

Prototype alumni database of the school deployed on Google App Engine and uses the Flask framework. Reads records from csv file and converts it into the datastore entries. 

App deployed live at [spsoldboys.appspot.com](http://spsoldboys.appspot.com/). Please note that it is still in Beta. 

* **Tech specs (Simple Flask Application on Google App Engine):** 
This application uses the Python Flask Skeleton for App Engine from Google provided [here](https://github.com/GoogleCloudPlatform/appengine-python-flask-skeleton)

##### Known and pending issues #####
* `cleanup.py`: 
		Year fails for some entries that are not entererd in the correct format. Eg. The following case will fail for entries after 2009.
		
```python

	if (len(str(year)) == 2):
		return str(str(19) + str(year))
```

* Errors due to GAE datastore's daily read/write quota limit needs to be handled.

* Minor bugs (CSS and otherwise)