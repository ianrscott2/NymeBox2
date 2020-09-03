header = os.popen("cat ./NymeBox_header.htm").read()

html = """

<!DOCTYPE HTML>
<html>
<title>Welcome to NymeBox</title>
<style>
.FTP{
  background-color: """ + ftpStatus[0] + """;
  border: none;
  color: black;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  width: 250px;
}

</style>
<body>
""" + str(header) + """
<br>
Send files to """ + FTP_URL[0] + """
<P>
<form action="NymeBox.py" name="FTP" method="POST">
	<input type="checkbox" name="JPG" value="JPG" """ + JPGisChecked + """>JPG
	<input type="checkbox" name="GIF" value="GIF" """ + GIFisChecked + """>GIF
	<input type="checkbox" name="NEF" value="NEF" """ + NEFisChecked + """>NEF<br>
	<input type="submit" value="Send via FTP" class="FTP">
</form>
</body>
</html>
"""

print("Content-type: text/html")
print
print(html)
