import json
import os.path

class HistoryConfig:
    PREV_RECORD_LOCATION = r'.\forecast_history.json'

class HistoryClient:
    def __init__(self, config):
        self.config = config

    def load_history(self):
        if os.path.exists(HistoryConfig.PREV_RECORD_LOCATION):
            self.history = json.load(open(HistoryConfig.PREV_RECORD_LOCATION))
        else:
            self.history = {}
    
    def update_history(self, pub_date, new_data):
        if pub_date not in self.history:
            self.history[pub_date] = new_data
        else:
            print('No new data')
    
    def save_history(self):
        json.dump(self.history, open(HistoryConfig.PREV_RECORD_LOCATION, 'w'), indent=4)