ALLOWED_HOSTS = ['www.worksmartevents.com', '127.0.0.1', '172.16.64.91']

DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'wse',                      # Or path to database file if using sqlite3.
                'USER': 'root',                      # Not used with sqlite3.
                'PASSWORD': 'root',                  # Not used with sqlite3.
                'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            },
}
