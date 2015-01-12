
README
-------

Overview

Capture is our front end for managing social media captures. This project will include largely just the front-end django application 
for this, but there is an entire set of scripts and tools being leveraged behind the scenes that this will communicate with. 


Setup
-----

1. Create a local database, and, if necessary, a special user
2. local.py settings file:
	1. In capture/settings create a local.py 
	2. Add the following code at the top to import the base settings:

			from base import *

	3. Generate a new SECRET_KEY. This can be done at: http://www.miniwebtool.com/django-secret-key-generator/
	4. Define SECRET_KEY beneath the previous line like so:

			SECRET_KEY = '<<code you generated>>'

	5. Override any values from base.py as necessary. These include DEBUG, TEMPLATE_DEBUG, and ALLOWED_HOSTS. 
	6. Add a DATABASE value for your appropriate config. The default sqllite3 version from django 1.7 is: 

			DATABASES = {
			    'default': {
			        'ENGINE': 'django.db.backends.sqlite3',
			        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
			    }
			}

		This has been removed from base.py to force you to enter a database. Consult the django documentation for information on this

	7. Run: python manage.py createsuperuser

3. Run the following command:

		python manage.py migrate

4. Update the path in capture/wsgi.py
5. Using the django admin, add a `capture_client` with the following permissions: `job modification - add`, `update - add`, `update - modify`. 



Auth Setup
--------------

For Apache and mod_wsgi, you need to enable Passing of the Authorization information. You can do this by adding `WSGIPassAuthorization On` for the serversr WSGI configuration. You can read more about this here: http://www.django-rest-framework.org/api-guide/authentication/#apache-mod_wsgi-specific-configuration


Django modifications
---------------------
I've made several modifications to django to better support dev and production environments. These are detailed below. 

manage.py:
	* changed the config location to point to capture/settings/local.py


