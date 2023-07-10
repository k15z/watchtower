import json
from google_play_scraper import app

result = app(
    'dev.kevz.ao3_disco',
    lang='en', # defaults to 'en'
    country='us' # defaults to 'us'
)

print(json.dumps(result, indent=2))

# https://itunes.apple.com/lookup?id=[...]&country=US&entity=software