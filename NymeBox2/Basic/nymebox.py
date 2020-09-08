class NymeBox_Core:

    def __init__(self):
        self.data = []

    def do_ftp(config):
    
        import ftplib
        import os
        import datetime
        import time
        import re
        import cgi
        import glob
        import sys

        nymeLogFile = './FTP_Progress.txt'
        nymeLog    = open(nymeLogFile, 'w+')
        #FTPUser = 'ftpuser'
        #FTPPassword = 'ftpuser'
        #SourceDir = '/var/www/NymeBox/SDCARD/**'
        #SourceDir = 'C:\\Users\\Ian\\Pictures\\NymeBox\\'
        process_mode = 'PROD'
        #DestDir = 'NymeBox/'
        #FtpURL = 'trek'

        time = datetime.datetime.utcnow()
        nymeLog.write(str(time) + "\n")
        time = str(time.strftime("%d%b%Y%H%M%S"))
        
        nymeLog.write("FTP URL is:          " + config.FtpURL + "\n")
        nymeLog.write("FTP User is:         " + config.FTPUser + "\n")
        nymeLog.write("FTP Password is:     " + config.FTPPassword + "\n")
        nymeLog.write("Destination Dir is:  " + config.DestDir + "\n")
        nymeLog.write("Source Dir is:       " + config.SourceDir + "\n")
        nymeLog.write("File Type List is:   " + config.FileTypeList + "\n")

        config.FtpURL = config.FtpURL.replace('ftp://', '')
        nymeLog.write("Udpated FTP URL is:  " + config.FtpURL + "\n")

        mediaListNum = 0
        mediaList = []

        if config.FileTypeList != "":
            for fileType in config.FileTypeList.split(","):
                nymeLog.write("Looking for fileType " + fileType + "\n")
                mediaFileList = glob.iglob(config.SourceDir + fileType, recursive=True)
                for filename in mediaFileList:
                    nymeLog.write("Looking at file " + filename + " in " + str(mediaFileList) + "\n")
                    if re.search("." + fileType + '$', filename, re.IGNORECASE):
                        nymeLog.write("Found the file " + filename + " in the directory " + config.SourceDir + "\n")
                        mediaListNum += 1
                        mediaList.append(filename)
                    else:
                        nymeLog.write("Didn't find any " + fileType + " media files in " + config.SourceDir + "\n")

        n=0
        try:
            nymeLog.write("Executing FTP Connection: " + str(ftp) + "\n")
            ftp = ftplib.FTP(config.FtpURL)
        except:
            nymeLog.write("Unable to connect to FTP Server, exiting...\n")
            nymeLog.close()
            return

        ftp.login(config.FTPUser,config.FTPPassword)
        ftp.cwd(config.DestDir)

        for eachPic in mediaList:
            if eachPic != "":
                file_name, file_extension = os.path.splitext(eachPic)
                eachPicDest = str(time) + "-" + str(n) + file_extension
                nymeLog.write(str(n+1) + " of " + str(mediaListNum) + " : Trying to send " + eachPic + " to " + config.DestDir + "/" + eachPicDest + "\n")
                file = open(eachPic, 'rb')
                ftp.storbinary('STOR ' + eachPicDest, fp=file)
                if process_mode == 'PROD':
                    os.rename(eachPic,eachPic + '.moved')                
                file.close()
            n=n+1
        ftp.quit()
        nymeLog.close()
        