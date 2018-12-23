from year_spreadsheet import YearSheet

"""****************************************************************************
To give user an interface for Google Sheets
****************************************************************************"""
class SheetsUI(object):

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


    def __init__(self):
        self.name = ""

    # Get the names of files that the user wants to add to yearly information
    def get_files(self):
        file_names = raw_input("Insert any file names you want to update" \
            "the monthly and yearly totals with here: ")
        self.file_list = file_names.replace(",", " ").split()

    def get_user_list(self):
        users = raw_input("Who should these files be shared with? " \
                          "(please give the email address of the users): ")
        self.user_list = users.replace(",", " ").split()

    # For every year represented in the files given by the user, extract
    # the months that go to every year
    def parse_months(self):
        self.month_map = {}
        for files in self.file_list:
            year_found = False
            month_found = False
            date = files.replace("/", "-").replace(".", "-").split("-")

            for key_year in self.month_map:
                if date[self._year] == key_year:
                    year_found = True
                    for month in self.month_map[key_year]:
                        if self._abbr_map[date[self._month]] == month:
                            month_found = True

            if not year_found:
                year = [self._abbr_map[date[self._month]]]
                self.month_map[date[self._year]] = year
            elif year_found and not month_found:
                self.month_map[date[self._year]].append(
                                            self._abbr_map[date[self._month]])

        for key_year in self.month_map:
            self.month_map[key_year].sort()

    # For every year represented in the files given by the user, extract
    # the files that go to every year
    def parse_files(self):
        self.file_map = {}
        year_found = False
        for this_file in self.file_list:
            date = this_file.replace("/", "-").replace(".", "-").split("-")

            for key_year in self.file_map:
                if date[self._year] == key_year:
                    year_found = True

            if not year_found:
                year = [this_file]
                self.file_map[date[self._year]] = year
            elif year_found:
                self.file_map[date[self._year]].append(this_file)

    # get data from user and store as member data
    def get_user_info(self):
        self.get_files()
        self.get_user_list()

    # Break up and store user given data into 'years and months'
    # and 'year and files'
    def parse_user_data(self):
        self.parse_months()
        self.parse_files()

    # for every year pass the year, a month list, file list, and user list.
    # The Year objects will take care of updating themselves.
    def update_sheets(self):
        self.year_list = self.month_map.keys()
        for year in self.year_list:
            year_sheet = YearSheet(year,
                                   self.month_map[year],
                                   self.file_map[year],
                                   self.user_list
                                   )
            year_sheet.update()

    # main function for SheetsUI
    def run(self):
        self.get_user_info()
        self.parse_user_data()
        self.update_sheets()
