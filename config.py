import os

# URL's
MITE_BASE_URL = 'https://foryouandyourcustomers.mite.yo.lk'
MITE_URL_TIME_ENTRIES = f'{MITE_BASE_URL}/time_entries.json'

# Authentication
MITE_API_KEY = os.environ.get('MITE_API_KEY')