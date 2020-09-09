class NymeBox_Core:

    def __init__(self, config):
        self.config = config

    def do_ftp(self):
    
        import ftplib
        import os
        import datetime
        import time
        import re
        import cgi
        import glob
        import sys

        nymeLogFile = './/Basic//FTP_Progress.txt'
        nymeLog    = open(nymeLogFile, 'r+')
        #SourceDir = '/var/www/NymeBox/SDCARD/**'
        #SourceDir = 'C:\\Users\\Ian\\Pictures\\NymeBox\\'
        process_mode = 'TEST'
        #process_mode = 'PROD'


        time = datetime.datetime.utcnow()
        nymeLog.write(str(time) + "\n")
        time = str(time.strftime("%d%b%Y%H%M%S"))
        
        nymeLog.write("FTP URL is:          " + self.config.FtpURL + "\n")
        nymeLog.write("FTP User is:         " + self.config.FTPUser + "\n")
        nymeLog.write("FTP Password is:     " + self.config.FTPPassword + "\n")
        nymeLog.write("Destination Dir is:  " + self.config.DestDir + "\n")
        nymeLog.write("Source Dir is:       " + self.config.SourceDir + "\n")
        nymeLog.write("File Type List is:   " + self.config.FileTypeList + "\n")

        self.FtpURL = self.FtpURL.replace('ftp://', '')
        nymeLog.write("Udpated FTP URL is:  " + self.FtpURL + "\n")
        self.FtpURL = 'trek'

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

        n=0
        try:
            nymeLog.write("Executing FTP Connection to: " + self.config.FtpURL + "\n")
            ftp = ftplib.FTP(self.FtpURL)
        except:
            nymeLog.write("Unable to connect to FTP Server " + self.config.FtpURL + ", exiting...\n")
            nymeLog.close()
            return

        nymeLog.write("Connected to: " + self.FtpURL + "\n")
        ftp.login(self.config.FTPUser,self.config.FTPPassword)
        ftp.cwd(self.config.DestDir)

        nymeLog.write("List of files to send: " + str(mediaList) + "\n")

        for eachPic in mediaList:
            nymeLog.write("Preparing to send: " + eachPic + "\n")
            if eachPic != "":
                file_name, file_extension = os.path.splitext(eachPic)
                eachPicDest = str(time) + "-" + str(n) + file_extension
                nymeLog.write(str(n+1) + " of " + str(mediaListNum) + " : Trying to send " + eachPic + " to " + self.config.DestDir + "/" + eachPicDest + "\n")
                file = open(eachPic, 'rb')
                ftp_status = ftp.storbinary('STOR ' + eachPicDest, fp=file)
                file.close()
                nymeLog.write(ftp_status)
                if process_mode == 'PROD':
                    nymeLog.write("Process Mode is " + process_mode + ". Moving " + eachPic + ".\n")
                    os.rename(eachPic,eachPic + '.moved')
                else:
                    nymeLog.write("Process Mode is " + process_mode + ". NOT Moving " + eachPic + ".\n")
            else:
                nymeLog.write("No more files to move.\n")
                    
                                    

            n=n+1
        ftp.quit()
        nymeLog.close()
        