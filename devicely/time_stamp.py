"""
TimeStamp for Android allows you to record the timestamp of an event at the time
it occurs. It also allows you to create specific tags such as "Running" or
"Walking" and timestamp those specific activities.
"""

import random

import pandas as pd

class TimeStampReader:
    """
    Read, timeshift and write data generated by the Android app TimeStamp

    Attributes
    ----------
    data : DataFrame
        DataFrame with datetime index and 'tag' column.
    """

    def __init__(self, path):
        """
        Read the csv generated by the app and saves the parsed DataFrame.

        Parameters
        ----------
        path : str
        """

        self.data = pd.read_csv(path, names=['tag_number', 'time', 'tag'])
        self.data['time'] = pd.to_datetime(self.data['time'], format='%Y/%m/%d(%a) %H:%M:%S')
        self.data.set_index('time', inplace=True, verify_integrity=True)
        self.data.sort_index(inplace=True)

    def write(self, path):
        """
        Write the DataFrame stored in 'data' to 'path'
        in the same format as it was read.

        Parameters
        ----------
        path : str
            Path to writing csv. Writing mode: 'w'
        """

        df_to_write = self.data.reset_index()[['tag_number', 'time', 'tag']]
        df_to_write.time = df_to_write.time.dt.strftime("%Y/%-m/%-d(%a)\u3000%H:%M:%S").str.lower()
        df_to_write.to_csv(path, header=None, index=None)

    def timeshift(self, shift='random'):
        """
        Timeshift the data by shifting the index.

        Parameters
        ----------
        shift : None/'random', pd.Timestamp or pd.Timedelta
            If shift is not specified, shifts the 'time' column by a random time
            interval between one month and two years to the past.

            If shift is a timdelta, shift the index by that timedelta.

            If shift is a timestamp, shifts the data such that the earliest entry
            has that timestamp. The remaining values will mantain the same
            time difference to the first entry.
        """

        if shift == 'random':
            one_month = pd.Timedelta('30 days').value
            two_years = pd.Timedelta('730 days').value
            random_timedelta = - pd.Timedelta(random.uniform(one_month, two_years)).round('s')
            self.timeshift(random_timedelta)
        if isinstance(shift, pd.Timedelta):
            self.data.index += shift
        if isinstance(shift, pd.Timestamp):
            timedeltas = self.data.index - self.data.index[0]
            self.data.index = shift + timedeltas