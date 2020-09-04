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
        import sys

        nymeLogFile = './FTP_Progress.txt'
        FTPUser = 'ftpuser'
        FTPPassword = 'ftpuser'
        nymeLog    = open(nymeLogFile, 'w+')
        source_dir = '/var/www/NymeBox/SDCARD/**'
        source_dir = 'C:\\Users\\Ian\\Pictures\\NymeBox\\'
        process_mode = 'TEST'
        dest_dir = 'NymeBox/'
        FtpURL = 'trek'

        time = datetime.datetime.utcnow()
        nymeLog.write(str(time) + "\n")
        time = str(time.strftime("%d%b%Y%H%M%S"))
        
        nymeLog.write("Executing the NymeBox Code! " + FtpURL + "," + FTPUser + "," + FTPPassword + "," + dest_dir + "," + source_dir + "," + FileTypeList + "\n")

        #ftp = ftplib.FTP(FtpURL)
        #ftp.login(FTPUser,FTPPassword)
        #ftp.cwd(dest_dir)

        #nymeLog.write("Executing FTP Connection: " + str(ftp) + "\n")

        mediaListNum = 0
        mediaList = []
        #FileTypeList = FileTypeList.split(",")

        if FileTypeList != "":
            for fileType in FileTypeList.split(","):
                nymeLog.write("Looking for fileType " + fileType + "\n")
                mediaFileList = glob.iglob(source_dir + fileType, recursive=True)
                for filename in mediaFileList:
                    nymeLog.write("Looking at file " + filename + " in " + str(mediaFileList) + "\n")
                    if re.search("." + fileType + '$', filename, re.IGNORECASE):
                        nymeLog.write("Found the file " + filename + " in the directory " + source_dir + "\n")
                        mediaListNum += 1
                        mediaList.append(filename)
                    else:
                        nymeLog.write("Didn't find any " + fileType + " media files in " + source_dir + "\n")

        n=0
        
        for eachPic in mediaList:
            if eachPic != "":
                file_name, file_extension = os.path.splitext(eachPic)
                eachPicDest = str(time) + "-" + str(n) + file_extension
                nymeLog.write(str(n+1) + " of " + str(mediaListNum) + " : Trying to send " + eachPic + " to " + destRootDir + "/" + eachPicDest + "\n")
                file = open(eachPic, 'rb')
                ftp.storbinary('STOR ' + eachPicDest, fp=file)
                if process_mode == 'PROD':
                    os.rename(eachPic,eachPic + '.moved')
			    file.close()
            n=n+1
        ftp.quit()
        nymeLog.close()
        