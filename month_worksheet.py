import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from container_func import list_union
from date_data import WeeklyData

# json credentials you downloaded earlier
scope = [
         'https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'
        ]

# get email and key from cred
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

# authenticate with Google
file = gspread.authorize(credentials)

"""***********************************************************************
MonthSheet class represents a worksheet added to the YearSheet totals'
spreadsheet
***********************************************************************"""
class MonthSheet(object):

    _wednesday = 0
    _women_rock = 1
    _nine_am = 2
    _eleven_am = 3
    _spanish = 4
    _special = 5
    _total = 6

    _buses = 0
    _stops = 1
    _riders = 2

    # Each MonthSheet object will have access to the Spreadsheet that it's
    # attached to. It will also have a corresponding list of files from where
    # it gets its data
    def __init__(self, month, year, parent_sheet, file_list):
        self.month = month
        self.year = year
        self.parent_sheet = parent_sheet
        self.file_list = file_list

    # Creates the header rows for each "month" worksheet
    def set_header_rows(self, this_sheet):
        header_row = this_sheet.range('A7:D7')
        header_row_values = ["WEEKLY SERVICES",
                             "NUMBER OF BUSES",
                             "NUMBER OF STOPS",
                             "TOTAL RIDERS"]
        i = 0
        for cell in header_row:
            cell.value = header_row_values[i]
            i += 1

        this_sheet.update_cells(header_row)

    # create a the title column
    def set_header_cols(self, this_sheet):
        service_col = this_sheet.range('A8:A14')
        service_col_values = ["Wed", "WR", "9 AM", "11 AM",
                              "SPANISH", "SPECIAL", "TOTAL"]

        i = 0
        for cell in service_col:
            cell.value = service_col_values[i]
            i += 1

        this_sheet.update_cells(service_col)

    # Update header rows and columns
    def add_template(self, this_sheet):
        self.set_header_rows(this_sheet)
        self.set_header_cols(this_sheet)

    # Create WeeklyData objects for each file associated with the month.
    # Add these objects to this months data_list data member
    def get_weekly_data(self):
        self.data_list = []
        for this_file in self.file_list:
            week_data = WeeklyData(this_file)
            self.data_list.append(week_data)

    # For each weekly spreadsheet, retrieve the relevant values
    def get_numbers(self):
                  #wed, wr, 9am, 11am, span, spec, tot
        self.buses =  [0,  0,   0,   0,     0,   0,    0]
        self.stops =  [0,  0,   0,   0,     0,   0,    0]
        self.riders = [0,  0,   0,   0,     0,   0,    0]

        for data_object in self.data_list:
            data = data_object.get_data()
            for i in range(7):
                self.buses[i] += data[self._buses][i]
                self.stops[i] += data[self._stops][i]
                self.riders[i] += data[self._riders][i]

    # Return all dates written on file for this month
    def get_files(self):
        self.date_file = self.month + " \'" + self.year + " files.txt"
        if os.path.exists(self.date_file):
            # if there exists a file of dates for this month
            try:
                read_file = open(self.date_file, "r")
                dates_on_file = read_file.read().splitlines()
                read_file.close()
                self.file_list = list_union(dates_on_file, self.file_list)

                write_file = open(self.date_file, "w")

            except IOError:
                print "shouldn't happen"

        else:
            # if the file doesn't exist, create one
            write_file = open(self.date_file, "w+")

        # write the list of weekly sheets used for data in this month to file
        for this_file in self.file_list:
            write_file.write(this_file)
            write_file.write("\n")
        write_file.close()

    # If a worksheet for this month hasn't been created, make one
    # otherwise get it. From the worksheet get the values range
    def get_worksheet(self):
        try:
            self.this_sheet = self.parent_sheet.worksheet(self.month)
            self.add_template(self.this_sheet)
        except gspread.WorksheetNotFound:
            self.this_sheet = self.parent_sheet.add_worksheet(self.month, 30, 10)
            self.add_template(self.this_sheet)

    # From file names in a month get the weekly data objects and numbers
    # asscociated with them.
    def get_month_data(self):
        self.get_weekly_data()
        self.get_numbers()

    def update_worksheet(self):
        data_cells = self.this_sheet.range('B8:D14')

        i = 0
        for cell in data_cells:
            if i % 3 == 0:
                cell.value = str(self.buses[i/3])
            if i % 3 == 1:
                cell.value = str(self.stops[i/3])
            if i % 3 == 2:
                cell.value = str(self.riders[i/3])

            i += 1

        self.this_sheet.update_cells(data_cells)

    # Main function to run for a MonthSheet object. It updates the files on
    # record to include the files passed to it, gets data sheets (and numbers)
    # for every data sheet associated, and then
    def update(self):
        self.get_files()
        self.get_worksheet()
        self.get_month_data()
        self.update_worksheet()
