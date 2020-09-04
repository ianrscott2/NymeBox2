class NymeBox_Core:

    def __init__(self):
        self.data = []

    def do_ftp(FtpURL, FileTypeList):

        import ftplib
        import os
        import datetime
        import time
        import re
        import cgi
        import glob

        nymeLogFile = './FTP_Progress.txt'
        FTPUser = 'ftpuser'
        FTPPassword = 'ftpuser'
        nymeLog    = open(nymeLogFile, 'w+')
        source_dir = '/var/www/NymeBox/SDCARD/**'
        process_mode = 'TEST'
        dest_dir = 'NymeBox'
        FtpURL = 'trek'

        time = datetime.datetime.utcnow()
        nymeLog.write(str(time) + "\n")
        time = str(time.strftime("%d%b%Y%H%M%S"))
        
        nymeLog.write("Executing the NymeBox Code! " + FtpURL + "," + FTPUser + "," + FTPPassword + "," + dest_dir + "," + source_dir + "," + FileTypeList)

        ftp = ftplib.FTP(FtpURL)
        ftp.login(FTPUser,FTPPassword)
        ftp.cwd(dest_dir)

        mediaListNum = 0
        mediaList = []

        if fileTypeList != "":
            for fileType in fileTypeList:
                #print("Looking for fileType " + fileType)
                for filename in glob.iglob(source_dir, recursive=True):
                    if re.search('.' + fileType + '$', filename, re.IGNORECASE):
                        mediaListNum += 1
                        mediaList.append(filename)

        c = conn.cursor()

        nymeLog.write("Executing FTP Connection: " + str(ftp))