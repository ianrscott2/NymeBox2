#!/usr/bin/python

import ftplib
import os
import datetime
import time
import re
import cgi

form = cgi.FieldStorage()

fileTypeList = []

c = conn.cursor()
if JPGFiles == "JPG":
	c.execute("UPDATE configuration SET VALUE = 'Yes' WHERE PROPERTY = 'JPGChecked'")
	fileTypeList.append('JPG')
else:
	c.execute("UPDATE configuration SET VALUE = 'No' WHERE PROPERTY = 'JPGChecked'")

if NEFFiles == "NEF":
	c.execute("UPDATE configuration SET VALUE = 'Yes' WHERE PROPERTY = 'NEFChecked'")
	fileTypeList.append('GIF')
else:
	c.execute("UPDATE configuration SET VALUE = 'No' WHERE PROPERTY = 'NEFChecked'")

if GIFFiles == "GIF":
	c.execute("UPDATE configuration SET VALUE = 'Yes' WHERE PROPERTY = 'GIFChecked'")
	fileTypeList.append('NEF')
else:
	c.execute("UPDATE configuration SET VALUE = 'No' WHERE PROPERTY = 'GIFChecked'")
conn.commit()


c = conn.cursor()
c.execute("SELECT VALUE FROM configuration WHERE PROPERTY = 'JPGChecked'")
JPGChecked = ([(r[0]) for r in c.fetchall()])
conn.commit()
c = conn.cursor()
c.execute("SELECT VALUE FROM configuration WHERE PROPERTY = 'GIFChecked'")
GIFChecked = ([(r[0]) for r in c.fetchall()])
conn.commit()
c = conn.cursor()
c.execute("SELECT VALUE FROM configuration WHERE PROPERTY = 'NEFChecked'")
NEFChecked = ([(r[0]) for r in c.fetchall()])
conn.commit()

c = conn.cursor()
c.execute("SELECT VALUE FROM configuration WHERE PROPERTY = 'URL'")
FTP_URL = [(r[0]) for r in c.fetchall()]


nymeLog    = open('./NymeBox_Output.htm', 'w')
user       = "ftpuser"
passwd     = "ftpuser"
destRootDir    = "/NymeBox"
destserver = FTP_URL[0]

ftp    = ftplib.FTP(destserver)
ftp.login(user,passwd)
ftp.cwd(destRootDir)

import glob

#unmountSD = os.popen("sudo umount /var/www/NymeBox/SDCARD").read()
#mountSD = os.popen("sudo mount -t none -o bind,rwx /dev/sda /var/www/NymeBox/SDCARD").read()

mediaListNum = 0
mediaList = []

if fileTypeList != "":
	for fileType in fileTypeList:
		#print("Looking for fileType " + fileType)
		for filename in glob.iglob('/var/www/NymeBox/SDCARD/**', recursive=True):
			if re.search('.' + fileType + '$', filename, re.IGNORECASE):
				mediaListNum += 1
				mediaList.append(filename)

c = conn.cursor()

time = datetime.datetime.utcnow()
nymeLog.write(str(time) + "\n")
time = str(time.strftime("%d%b%Y%H%M%S"))
#nymeLog.write(str(fileTypeList))
#nymeLog.write('List of files to move are:\n')
#nymeLog.write(str(mediaList))
n=0
for eachPic in mediaList:
	if eachPic != "":
       		file_name, file_extension = os.path.splitext(eachPic)
       		eachPicDest = str(time) + "-" + str(n) + file_extension
       		nymeLog.write(str(n+1) + " of " + str(mediaListNum) + " : Trying to send " + eachPic + " to " + destRootDir + "/" + eachPicDest + "\n")
       		file = open(eachPic, 'rb')
       		ftp.storbinary('STOR ' + eachPicDest, fp=file)
    		#os.rename(eachPic,eachPic + '.moved')
       		file.close()
#    	else:
#      		nymeLog.write("No more files")
	n=n+1
ftp.quit()
nymeLog.close()
nymeLog    = open('./NymeBox_Output.htm', 'r')
nyme_output = "<pre>" + nymeLog.read() + "</pre>"
nymeLog.close()

header = os.popen("cat ./NymeBox_header.htm").read()

html_header = """
<!DOCTYPE HTML>
<html>
""" + header + """
<title>Welcome to NymeBox</title>
<body>
<p>OUTPUT</p>
"""

html_footer = """
</body>
</html>
"""

if mediaListNum == 0:
	c.execute("UPDATE configuration set VALUE = 'red' WHERE PROPERTY = 'checkStatus'")
	c.execute("UPDATE configuration set VALUE = 'red' WHERE PROPERTY = 'ftpStatus'")
else:
	c.execute("UPDATE configuration set VALUE = 'green' WHERE PROPERTY = 'checkStatus'")
	c.execute("UPDATE configuration set VALUE = 'green' WHERE PROPERTY = 'ftpStatus'")
conn.commit()

print("Content-type: text/html")
print(html_header)
print(nyme_output)
print(html_footer)
