from config.settings.local import *

# Causes API to send info in API response, instead of Email or SMS etc. for testing automation.
TEST_MODE = True

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}
