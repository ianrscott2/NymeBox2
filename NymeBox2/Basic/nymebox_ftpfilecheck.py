class NymeBox_Check:

    def __init__(self, config):
        self.config = config

    def check_ftp_files(self):
    
        import os
        import datetime
        import time
        import re
        import cgi
        import glob
        import sys

        nymeLogFile = './/Basic//FTP_FileCheck.txt'
        nymeLog    = open(nymeLogFile, 'w')
        #SourceDir = '/var/www/NymeBox/SDCARD/**'
        #SourceDir = 'C:\\Users\\Ian\\Pictures\\NymeBox\\'
        #process_mode = 'PROD'

        time = datetime.datetime.utcnow()
        nymeLog.write(str(time) + "\n")
        time = str(time.strftime("%d%b%Y%H%M%S"))
        
        nymeLog.write("Source Dir is:       " + self.config.SourceDir + "\n")
        nymeLog.write("File Type List is:   " + self.config.FileTypeList + "\n")

        mediaListNum = 0
        mediaList = []

        if self.config.FileTypeList != "":
            for fileType in self.config.FileTypeList.split(","):
                nymeLog.write("Looking for fileType " + fileType + "\n")
                mediaFileList = glob.iglob(self.config.SourceDir + fileType, recursive=True)
                for filename in mediaFileList:
                    nymeLog.write("Looking at file " + filename + " in " + str(mediaFileList) + "\n")
                    if re.search("." + fileType + '$', filename, re.IGNORECASE):
                        nymeLog.write("Found the file " + filename + " in the directory " + self.config.SourceDir + "\n")
                        mediaListNum += 1
                        mediaList.append(filename)
                    else:
                        nymeLog.write("Didn't find any " + fileType + " media files in " + self.config.SourceDir + "\n")

        nymeLog.write("List of files to send: " + str(mediaList) + "\n")


        nymeLog.close()
        