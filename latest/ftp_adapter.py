import ftplib


class FTPFile:

    def __init__(self, name, modify):
        self.name = name[1:]  # Removes a whitespace
        self.modify = modify
        self.date = int(self.parse_date())

    def parse_date(self):
        number_date = self.modify.split('=')
        return number_date[1]


# Numeric position of the required data in the array
NAME_POSITION = 7
DATE_POSITION = 2
# Server host and credentials. You can export to other files, or env variables
HOST = 'ftp.example.com'
HTTP_HOST = 'http://example.com'
USER = 'ftp_username'
PASS = 'ftp_password'
# Supported file types. More can be added to this list
FORMATS = ['zip', 'rar']


def connect():
    # Connects to the FTP server
    ftp = ftplib.FTP(HOST)
    ftp.login(user=USER, passwd=PASS)
    return ftp


def get_last_file_url(subdir: str):
    try:
        # Get connection
        ftp = connect()
        # Navigate to subdir
        if subdir is not None:
            ftp.cwd(subdir)
        # Get all data
        raw_data = []
        # Data separated with semi-colons
        ftp.retrlines('MLSD', raw_data.append)
        # Get files from raw_data
        files = files_from_raw_data(raw_data)

        files_list = []
        for file in files:
            print(file.name)
            files_list.append(file)

        # Sort list by date
        files_list = sorted(files_list, key=lambda x: x.date, reverse=True)
        # Return the latest file
        return files_list[0]
    except ftplib.error_perm:
        print('No such directory')
        return FTPFile(' Directory not found', 'modify=0')


def files_from_raw_data(raw_data):
    for line in raw_data:
        # Separate values
        values = line.split(';')
        name = values[NAME_POSITION]
        date = values[DATE_POSITION]
        if name.startswith(' .'):  # Metadata files not added
            continue
        name_split = name.split('.')
        length = len(name_split)
        if length < 2:  # It's a subdir, not a file
            continue
        if name_split[length - 1] not in FORMATS:  # Unwanted format
            continue
        # Create object file with name and date
        file = FTPFile(name, date)
        yield file
