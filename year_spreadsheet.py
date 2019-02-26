import json
import gspread
#from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from month_worksheet import MonthSheet

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

"""***********************************************************************
YearSheet represents each year of "weekly bus ministry numbers"
Each object will have a list of worksheets of months' totals and a total
worksheet
***********************************************************************"""
class YearSheet(object):

    _month = 0
    _day = 1
    _year = 2

    _abbr_map = {'1': 'Jan', '01': 'Jan',
                 '2': 'Feb', '02': 'Feb',
                 '3': 'Mar', '03': 'Mar',
                 '4': 'Apr', '04': 'Apr',
                 '5': 'May', '05': 'May',
                 '6': 'Jun', '06': 'Jun',
                 '7': 'Jul', '07': 'Jul',
                 '8': 'Aug', '08': 'Aug',
                 '9': 'Sep', '09': 'Sep',
                 '10': 'Oct',
                 '11': 'Nov',
                 '12': 'Dec'
                }

    # Constructor initializes the representative year, name of the spreadsheet,
    # list of months added to the year, list of files passed to the year, and
    # list of users who should have shared permissions with any created
    # yearly spreadsheet
    def __init__(self, year, month_list, file_list, user_list):
        self.year = year
        self.sheet_name = "\'" + year + " Totals"
        self.month_list = month_list
        self.file_list = file_list
        self.user_list = user_list
        self.value_range = 'B8:D14'

    # Separate the year's files into month, file_list pairings
    def parse_files(self):
        self.month_file_map = {}
        for month in self.month_list:
            self.month_file_map[month] = []
            for this_file in self.file_list:
                date = this_file.replace("/", "-").replace(".", "-").split("-")

                if self._abbr_map[date[self._month]] == month:
                    self.month_file_map[month].append(this_file)


    # Create or open a spreadsheet for the year and get as a data member.
    # Also sets the first worksheet as an empty "totals" sheet.
    def get_spreadsheet(self):
        try:
            #open existing file
            print "open existing"
            self.totals = file.open(self.sheet_name)
        except gspread.SpreadsheetNotFound:
            # create a year spreadsheet and share permission
            print "create spreadsheet"
            self.totals = file.create(self.sheet_name)
            for user in self.user_list:
                self.totals.share(user,
                                  perm_type = 'user',
                                  role = 'writer'
                                  )

        self.totals_sheet = self.totals.sheet1


    # For each month passed to this year, get the files for each month,
    # initialize month objects with them, and then update the objects
    def update_months(self):
        self.parse_files()
        for month in self.month_list:
            month_worksheet = MonthSheet(month,
                                        self.year,
                                        self.totals,
                                        self.month_file_map[month]
                                        )
        month_worksheet.update()
        totals_worksheet = MonthSheet('Sheet1',
                                      self.year,
                                      self.totals,
                                      self.month_file_map[month])
        totals_worksheet.add_template(self.totals_sheet)

    # Get information from all month worksheets and update totals worksheet
    def update_totals(self):
        totals_cells = self.totals_sheet.range(self.value_range)

        for cell in totals_cells:
            cell.value = 0

        self.totals_sheet.update_cells(totals_cells)

        month_sheet_values = []
        #get all worksheets for the spreadsheet
        month_sheet_list = self.totals.worksheets()
        for month_sheet in month_sheet_list:
        #for each worksheet
            #get the range of cells with data as a list
            data_cells = month_sheet.range(self.value_range)
            #add that list to the months' values
            month_sheet_values.append(data_cells)
            for cell, total_cell in zip(data_cells, totals_cells):
                total_cell.value += int(cell.value)

        self.totals_sheet.update_cells(totals_cells)

    # Main function to update the YearSheet object monthly and yearly totals
    def update(self):
        self.get_spreadsheet()
        self.parse_files()
        self.update_months()
        self.update_totals()
