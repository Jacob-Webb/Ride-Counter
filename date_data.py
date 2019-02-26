import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# json credentials you downloaded earlier
json_key = json.load(open('creds.json'))
scope = [
         'https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'
        ]

# get email and key from cred
credentials = ServiceAccountCredentials(json_key['client_email'],
                                            json_key['private_key'].encode(),
                                            scope
                                           )

# authenticate with Google
file = gspread.authorize(credentials)
"""****************************************************************************
WeeklyData class pulls the data from the weekly spreadsheets. This is the core
of the data that will be updated in the "totals" for the yearly spreadsheets.
****************************************************************************"""
class WeeklyData(object):

    #data members used to access buses, stops, and riders list elements
    _wednesday = 0
    _women_rock = 1
    _nine_am = 2
    _eleven_am = 3
    _spanish = 4
    _special = 5
    _total = 6

    _bus_index = 0
    _stop_index = 1
    _rider_index = 2

    # Initialize Week object by opening a file specific to the week and pulling
    # all of the relevant information from it
    def __init__(self,date_file):
        self.date_sheet = file.open(date_file).sheet1
        # info is a list of cell objects from left to right and
        # top to bottom in the range
        self.cell_list = self.date_sheet.range('B8:D14')
        """
        weekly_sheet.range cell values
                    buses   stops   Riders
            wed      0        1       2
            wr       3        4       5
            9 am     6        7       8
            11 am    9        10      11
            span     12       13      14
            special  15       16      17
            total    18       19      20
        """

        self.buses = []
        self.stops = []
        self.riders = []
        add_info = 0

        for cell in self.cell_list:
            if add_info % 3 == 0: # if the cell value is a multiple of 3, add to buses[]
                # if the value is not None add the value to the list
                if cell.value:
                    self.buses.append(int(cell.value))
                else:   # otherwise, add a zero
                    self.buses.append(0)
            elif add_info % 3 == 1: # if the cell is a multiple of 3 + 1 add to stops[]
                if cell.value:
                    self.stops.append(int(cell.value))
                else:
                    self.stops.append(0)
            elif  add_info % 3 == 2: # if the cell is a multiple of 3 + 2 add the cell to riders[]
                if cell.value:
                    self.riders.append(int(cell.value))
                else:
                    self.riders.append(0)

            add_info += 1

    # Retrieve the total values for the week
    def get_date_totals(self):
        totals = {
                  'Total Buses': self.buses[self._total],
                  'Total Stops': self.stops[self._total],
                  'Total Riders': self.riders[self._total]
                 }
        return totals

    # Retrieve all values for the week and add them to a dict
    def get_data(self):
        date_info = [
                        [self.buses[self._wednesday], self.buses[self._women_rock],
                         self.buses[self._nine_am], self.buses[self._eleven_am],
                         self.buses[self._spanish], self.buses[self._special],
                         self.buses[self._total]
                        ],
                        [self.stops[self._wednesday], self.stops[self._women_rock],
                         self.stops[self._nine_am], self.stops[self._eleven_am],
                         self.stops[self._spanish], self.stops[self._special],
                         self.stops[self._total]
                        ],
                        [self.riders[self._wednesday], self.riders[self._women_rock],
                         self.riders[self._nine_am], self.riders[self._eleven_am],
                         self.riders[self._spanish], self.riders[self._special],
                         self.riders[self._total]
                        ]
                       ]

        return date_info
