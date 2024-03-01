# logging implementation

import sys
import logging
import traceback

logging.basicConfig(
    filename=r'.\vic_fire_danger.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

def custom_excepthook(exc_type, exc_value, exc_traceback):
    # Do not print exception when user cancels the program
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("An uncaught exception occurred:")
    logging.error("Type: %s", exc_type)
    logging.error("Value: %s", exc_value)

    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            logging.error(repr(line))

sys.excepthook = custom_excepthook

# application implementation

from collections import defaultdict
import json

import requests
import win32com.client as win32

def main():
    cookies = {
        '_gcl_au': '1.1.143843960.1707732045',
        '_fbp': 'fb.3.1707732045368.414798629',
        'cfafirsttime': 'false',
        '_hjSessionUser_2759129': 'eyJpZCI6ImI4ZmMzZGU4LTlhZWMtNTViYy04MmU0LWFiNzhhNzJkYWRhNSIsImNyZWF0ZWQiOjE3MDc3MzIwNDYyOTcsImV4aXN0aW5nIjp0cnVlfQ==',
        'cfalocation': 'Woodend VIC 3442, Australia',
        'cfalat': '-37.3568266',
        'cfalon': '144.5273723',
        'cfasuburb': 'Woodend',
        'cfastate': 'VIC',
        'cfapostal': '3442',
        'cfacountry': 'Australia',
        'cfalocation': 'Woodend VIC 3442, Australia',
        'cfalon': '144.5273723',
        'cfalat': '-37.3568266',
        'cfasuburb': 'Woodend',
        'cfastate': 'VIC',
        'cfapostal': '3442',
        'cfacountry': 'Australia',
        'cfaFindWithInUseDefault': 'False',
        'ASP.NET_SessionId': 'bntfp42bxsd2yuosnmzz5st5',
        '__AntiXsrfToken': 'c08661e3d2024734933db11956106279',
        '_gid': 'GA1.4.354397308.1709320459',
        '_hjSession_2759129': 'eyJpZCI6IjJjOTllODViLTQxODYtNDhiZC04NDVjLTRjZGVhMTA2MWQ5ZSIsImMiOjE3MDkzMjA0NjE0MjQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_gat_UA-1847174-1': '1',
        '_gat_gtag_UA_1847174_1': '1',
        '_ga': 'GA1.4.279794893.1707732046',
        '_ga_4Y54F18WBL': 'GS1.1.1709320458.9.1.1709320629.42.0.0',
    }

    headers = {
        'authority': 'www.cfa.vic.gov.au',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-AU,en;q=0.9,en-GB-oxendict;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/json; charset=UTF-8',
        # 'cookie': '_gcl_au=1.1.143843960.1707732045; _fbp=fb.3.1707732045368.414798629; cfafirsttime=false; _hjSessionUser_2759129=eyJpZCI6ImI4ZmMzZGU4LTlhZWMtNTViYy04MmU0LWFiNzhhNzJkYWRhNSIsImNyZWF0ZWQiOjE3MDc3MzIwNDYyOTcsImV4aXN0aW5nIjp0cnVlfQ==; cfalocation=Woodend VIC 3442, Australia; cfalat=-37.3568266; cfalon=144.5273723; cfasuburb=Woodend; cfastate=VIC; cfapostal=3442; cfacountry=Australia; cfalocation=Woodend VIC 3442, Australia; cfalon=144.5273723; cfalat=-37.3568266; cfasuburb=Woodend; cfastate=VIC; cfapostal=3442; cfacountry=Australia; cfaFindWithInUseDefault=False; ASP.NET_SessionId=bntfp42bxsd2yuosnmzz5st5; __AntiXsrfToken=c08661e3d2024734933db11956106279; _gid=GA1.4.354397308.1709320459; _hjSession_2759129=eyJpZCI6IjJjOTllODViLTQxODYtNDhiZC04NDVjLTRjZGVhMTA2MWQ5ZSIsImMiOjE3MDkzMjA0NjE0MjQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gat_UA-1847174-1=1; _gat_gtag_UA_1847174_1=1; _ga=GA1.4.279794893.1707732046; _ga_4Y54F18WBL=GS1.1.1709320458.9.1.1709320629.42.0.0',
        'origin': 'https://www.cfa.vic.gov.au',
        'referer': 'https://www.cfa.vic.gov.au/warnings-restrictions/fire-bans-ratings-and-restrictions/total-fire-bans-fire-danger-ratings/central-fire-district',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'AdminEmailAddress': 'digitalworkflow@cfa.vic.gov.au',
    }

    response = requests.post('https://www.cfa.vic.gov.au/api/cfa/location/view/', cookies=cookies, headers=headers, json=json_data)

    new_forecasts = {}

    STATUS_MAP = {
        'status': {'N': 0, 'Y': 1},
        'rating': {'NO RATING': 0, 'HIGH': 1, 'EXTREME': 2, 'CATASTROPHIC': 3}
    }

    new_forecasts = [
        {'date': f['IssueDate'], 'issued_at': f['IssueAt'], 'status': STATUS_MAP['status'][f['Status']], 'rating': STATUS_MAP['rating'][f['DistrictRating']]}
        for f in response.json().get('FireBansAndRatingsDistrictWrapper',{})
    ]

    old_forecasts = json.load(open('vic_fire_danger/forecast_history.api.json'))
    old_forecasts.extend(new_forecasts)
    json.dump(list(set(old_forecasts)), open('vic_fire_danger/forecast_history.json', 'w'), indent=4)

    # if content:
    #     outlook = win32.Dispatch('outlook.application')
    #     mail = outlook.CreateItem(0)
    #     mail.To = 'tim.holmes@gww.com.au'
    #     mail.Subject = f'Fire Danger Alert ({content['date']})'
    #     mail.HTMLBody = content['body']
    #     mail.Send()

if __name__ == '__main__':
    main()