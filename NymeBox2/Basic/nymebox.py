class NymeBox_Core:

    def __init__(self, config):
        self.config = config

    def log_entry(self,log_file,severity,message):
        import os
        import sys

        print(severity + ": " + message)
        #print >>log_file, severity + ": " + message
        log_file.write(severity + ": " + message)

    def get_ftp_files(self):
    
        import os
        import datetime
        import time
        import glob
        import sys
        from pathlib import Path
        from .config import LOG_FILE_FOLDER

        nymeLogFile = LOG_FILE_FOLDER + 'FTP_FileCheck.txt'
        nymeLog    = open(nymeLogFile, 'w')
        nymeLog    = open(nymeLogFile, 'a')

        mediaList = []

        if self.config.FileTypeList != "":
            for fileType in self.config.FileTypeList.split(","):
                nymeLog.write("Looking for fileType " + fileType + "\n")
                newList = glob.glob(self.config.SourceDir + "/**/" + fileType, recursive=True)
                mediaList = mediaList + newList

        nymeLog.write("\nList of files to send: \n\n")
        nymeLog.writelines("%s\n" % mediaFile for mediaFile in mediaList)
        nymeLog.close()
        return mediaList
        
    def do_ftp(self):
    
        import ftplib
        import os
        import datetime
        import time
        import re
        import glob
        import sys
        from shutil import copyfile
        from .config import LOG_FILE_FOLDER
        
        FTPLogFile = LOG_FILE_FOLDER + 'FTP_Progress.txt'
        nymeLog    = open(FTPLogFile, 'w')
        

        time = datetime.datetime.utcnow()
        nymeLog.write(str(time) + "\n")
        time = str(time.strftime("%d%b%Y%H%M%S"))
                
        #nymeLog.write("FTP User is:         " + self.config.FTPUser + "\n")
        #nymeLog.write("Destination Dir is:  " + self.config.DestDir + "\n")
        #nymeLog.write("Source Dir is:       " + self.config.SourceDir + "\n")
        #nymeLog.write("File Type List is:   " + self.config.FileTypeList + "\n")

        self.config.FtpURL = self.config.FtpURL.replace('ftp://', '')
        
        filesToFTP = []
        #getftp = NymeBox_Core(config[0])
        filesToFTP = self.get_ftp_files()
         
        #nymeLog.writelines("\nThe list to FTP is: \n\n")
        #nymeLog.writelines("%s\n" % mediaFile for mediaFile in filesToFTP)

        try:
            nymeLog.write("Executing FTP Connection to: " + self.config.FtpURL + "\n")
            print("Executing FTP Connection to: " + self.config.FtpURL + "\n")
            ftp = ftplib.FTP(self.config.FtpURL)
        except:
            nymeLog.write("Unable to connect to FTP Server " + self.config.FtpURL + ", exiting...\n")
            print("Unable to connect to FTP Server " + self.config.FtpURL + ", exiting...\n")
            nymeLog.close()
            return

        nymeLog.write("Connected to: " + self.config.FtpURL + "\n")
        ftp.login(self.config.FTPUser,self.config.FTPPassword)
        ftp.cwd(self.config.DestDir)

        n=0
        message = "Mode is " + self.config.ProcMode + "\n\n"
        self.log_entry(nymeLog, "INFO", message)
        nymeLog.close()

        for eachPic in filesToFTP:
            nymeLog    = open(FTPLogFile, 'a')
            if eachPic != "":
                file_name, file_extension = os.path.splitext(eachPic)
                eachPicDest = str(time) + "-" + str(n) + file_extension
                file = open(eachPic, 'rb')
                ftp_status = ftp.storbinary('STOR ' + eachPicDest, fp=file)
                file.close()
                #nymeLog.write(ftp_status)
                justFileName = os.path.basename(file_name)
                message = "Moving " + justFileName + ".\n"
                self.log_entry(nymeLog, "INFO", message)
                if self.config.ProcMode == 'PROD':
                    os.rename(eachPic,eachPic + '.moved')
            else:
                nymeLog.write("No more files to move.\n")
            n=n+1
            nymeLog.close()
        ftp.quit()
        copyfile(FTPLogFile, FTPLogFile + '.last')
        
        