
# Press Shift+F10 to execute it or replace it with your code.

import api_secrets
import datetime
import pandas as pd
import requests

OPENING_DATE = "2022-03-12"

def catch_date(date):
    """Takes in user input for target date and transforms it to the desired output date format: 'YYYY-MM-DD' """
    pass

def request_manifest(date: str):
    """Function does URL Get request from iFly Manifest for the input argument 'date' as a string.
    'Date' string is formatted as YYYY-MM-DD"""
    url = api_secrets.url
    Headers = api_secrets.Headers
    cookies = api_secrets.cookies
    form_data = {"manifest_cache": "0", "formaction": "get_manifest", "date": str(date), "tunnel": "COSP"}
    return requests.get(url, headers=Headers, data=form_data, cookies=cookies)

class Manifest(dict):
    def __init__(self, date):
        self.date = str(date)
        self.response = request_manifest(self.date)
        self.json = self.response.json()['data']
        self.res_times = list(self.json.keys())
        self.res_times_flown = [time for time in self.res_times if self.json[time]['guests']]

    @property
    def guests(self):
        return dict(zip(self.guests_df['guest_no'], self.guests_df['name']))

    @property
    def guests_names(self):
        # Would be incorrect to name-appendices like 'Jr./junior/III' etc.
        sorted_guest_names = list(self.guests.values())
        sorted_guest_names.sort(key=lambda name: name.split()[-1])
        return sorted_guest_names

    @property
    def guests_nums(self):
        sorted_guest_nums = list(self.guests.keys())
        sorted_guest_nums.sort(key=int) # Sort in ascending order by guest number
        return sorted_guest_nums

    @property
    def guests_df(self):
        days_guests = []
        for time in self.res_times_flown:
            for guest in self.json[time]['guests']:
                days_guests.append(guest)
        return pd.DataFrame(days_guests)


# If continuing this, it still needs a function to loop over range of dates requested, bounded by OPENING_DATE

if __name__ == '__main__':
    opening_day = "2022-03-12"
    test_date = "2022-10-23"

