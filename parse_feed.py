import xml.etree.ElementTree as ET
from datetime import date, timedelta
from html.parser import HTMLParser

import requests

# data locations
class ForecastConfig:
    """Default configuration for the forecast"""
    # rss feed
    RSS_FEED = 'https://www.cfa.vic.gov.au/cfa/rssfeed/central-firedistrict_rss.xml'

    # day constants
    TODAY = date.today()
    TITLE_DT_FORMAT = '%A, %d %B %Y' # eg. Wednesday, 28 February 2024
    DAY_NAMES = ['Today', 'Tomorrow', 'In 2 days', 'In 3 days']
    RECORD_DT_FORMAT = '%Y-%m-%d'

    # total fire ban constants
    TFB_PHRASE = 'has been declared a day of Total Fire Ban'
    REGION = 'Central (includes Melbourne and Geelong)'

    # fire rating constants
    RATINGS = {
        'NO RATING': 0, 
        'MODERATE': 1, 
        'HIGH': 2, 
        'EXTREME': 3, 
        'CATASTROHPIC': 4
    }

class ParseDescription(HTMLParser):
    def __init__(self):
        self.data = []
        super().__init__()

    def feed(self, *args, **kwargs):
        super().feed(*args, **kwargs)
        return self
    
    def handle_data(self, data):
        self.data.append(data)

class ForecastClient:
    def __init__(self, config):
        self.config = config

    def get_latest_data(self):
        rss_feed_request = requests.get(self.config.RSS_FEED)
        rss_feed_request.encoding = rss_feed_request.apparent_encoding
        rss_feed_content = rss_feed_request.text

        rss_feed_tree = ET.fromstring(rss_feed_content) # parse the xml
        channel = rss_feed_tree.find('channel')
        pub_date = channel.find('pubDate').text
        items = channel.findall('item')[:-1] # last item is a summary

        return pub_date, items

    def parse_item(self, i, item):
        # check date
        title = item.find('title').text
        item_date = self.config.TODAY + timedelta(days=i)
        assert title == item_date.strftime(self.config.TITLE_DT_FORMAT), f'{title} != {item_date.strftime(self.config.TITLE_DT_FORMAT)}'

        # parse description
        description = item.find('description').text
        data = ParseDescription().feed(description).data

        # check TFB
        tfb_data = data[0] # first line is TFB
        tfb = (self.config.TFB_PHRASE in tfb_data) and (self.config.REGION in tfb_data)

        # check fire rating
        danger_rating_data = data[3] if data[3].startswith('Central: ') else data[2]  # third or fourth line is fire danger rating
        rating = danger_rating_data.split(' ')[-1]
        print(danger_rating_data, rating)
        if rating not in self.config.RATINGS:
            rating = 'NO RATING'

        item_data = {
            'tfb': tfb,
            'tfb_id': int(tfb),
            'rating': rating,
            'rating_id': self.config.RATINGS[rating],
        }

        return item_date.strftime(self.config.RECORD_DT_FORMAT), item_data

    def get_forecasts(self, items):
        return dict(self.parse_item(i, item) for i, item in enumerate(items))

