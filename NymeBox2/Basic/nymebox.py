class NymeBox_Core:

    def __init__(self, config):
        import socket
        self.config = config
        if 'nymebox' in socket.gethostname():
            self.app_mode = "PROD"
        else:
            self.app_mode = "TEST"

    def log_entry(self,log_file,severity,message):
        import os
        import sys

        current_log = severity + ": " + message
        print(current_log)
        #log_file.write(severity + ": " + message)
        return current_log

    def mount_sdcard(self):
        
        FTP_LogFile = ''

        import os
        import sys
        if os.name == 'posix':
            sd_dev = os.system("sudo fdisk -l | grep -E '^/dev/sd' | grep -Eo '^[^ ]+'")
            message = "Mounting " + str(sd_dev)
            self.log_entry(FTP_LogFile, "INFO", message)            
            os.system('mkdir ' + str(self.config.DestDir))
            os.system('sudo mount ' + str(sd_dev) + ' ' + str(self.config.DestDir) + ' 2> /dev/null')
            mounted = os.system('df -k | grep ' + self.config.DestDir)
            message = "Mount result is: " + str(mounted)
            self.log_entry(FTP_LogFile, "INFO", message)            
            if mounted:
                mount_drv = "Success"
            else:
                mount_drv = "Failed" 
        else:
            mount_drv = "Success"
        return mount_drv



    def get_ftp_files(self):
    
        import os
        import datetime
        import time
        import glob
        import sys
        from pathlib import Path
        from Basic.models import ConfigItem
        from django.db import connection

        mediaList = []
        FTP_LogFile = ''

        if self.config.FileTypeList != "":
            for fileType in self.config.FileTypeList.split(","):
                message = "Looking for fileType " + fileType + "\n"
                self.log_entry(FTP_LogFile, "INFO", message)
                newList = glob.glob(self.config.SourceDir + "/**/" + fileType.upper(), recursive=True, )
                mediaList = mediaList + newList
                newList = glob.glob(self.config.SourceDir + "/**/" + fileType.lower(), recursive=True, )
                mediaList = mediaList + newList
                
                fileList = '\n'.join(mediaList)
            fileListUpdate = "UPDATE basic_configitem SET MovedFiles = %s WHERE ProcMode = %s;"
            with connection.cursor() as cursor:
                  cursor.execute(fileListUpdate, [fileList, self.app_mode])
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
        from django.db import connection

        FTP_LogFile = ''
        current_log = ''
        time = datetime.datetime.utcnow()
        message = str(time) + "\n"
        current_log =  current_log + self.log_entry(FTP_LogFile, "INFO", message)
        time = str(time.strftime("%d%b%Y%H%M%S"))

        self.config.FtpURL = self.config.FtpURL.replace('ftp://', '')
        
        filesToFTP = []
        filesToFTP = self.get_ftp_files()

        try:
            message = "Executing FTP Connection to: " + self.config.FtpURL + "\n"
            current_log =  current_log + self.log_entry(FTP_LogFile, "INFO", message)
            ftp = ftplib.FTP(self.config.FtpURL)
        except:
            message = "Unable to connect to FTP Server " + self.config.FtpURL + ", exiting...\n"
            current_log =  current_log + self.log_entry(FTP_LogFile, "INFO", message)
            fileListUpdate = "UPDATE basic_configitem SET LastLog = %s WHERE ProcMode = %s;"
            with connection.cursor() as cursor:
                cursor.execute(fileListUpdate, [current_log, self.app_mode])
            return current_log, 'ERROR'

        message = "Connected to: " + self.config.FtpURL + "\n"
        current_log =  current_log + self.log_entry(FTP_LogFile, "INFO", message)
        ftp.login(self.config.FTPUser,self.config.FTPPassword)
        ftp.cwd(self.config.DestDir)

        n=0
        message = "Mode is " + self.config.ProcMode + "\n\n"
        current_log =  current_log + self.log_entry(FTP_LogFile, "INFO", message)

        for eachPic in filesToFTP:
            
            if eachPic != "":
                file_name, file_extension = os.path.splitext(eachPic)
                eachPicDest = str(time) + "-" + str(n) + file_extension
                message = "File is " + file_name + "\n"
                current_log = current_log +  self.log_entry(FTP_LogFile, "INFO", message)
                file = open(eachPic, 'rb')
                ftp.storbinary('STOR ' + eachPicDest, fp=file)
                file.close()
                #FTP_LogFile.write(ftp_status)
                justFileName = os.path.basename(file_name)
                message = "Moving " + justFileName + ".\n"
                current_log = current_log + self.log_entry(FTP_LogFile, "INFO", message)
                if self.config.ProcMode == 'PROD':
                    os.rename(eachPic,eachPic + '.moved')
            n=n+1   
        ftp.quit()
        fileListUpdate = "UPDATE basic_configitem SET LastLog = %s WHERE ProcMode = %s;"
        with connection.cursor() as cursor:
            cursor.execute(fileListUpdate, [current_log, self.app_mode])
        return current_log, 'Success'
        
        