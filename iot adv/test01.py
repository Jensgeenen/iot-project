#!/usr/bin/python
#Import modules for CGI handling
import cgi , cgitb
cgitb.enable()
#Create instance .
form = cgi.FieldStorage()
# Get data from url fields
first_value = form.getvalue ("first_value")
second_value = form.getvalue ("second_value")
print ( "Content-type:text/html\n\n")
print ( "<head>")
print ("<title> get cgi program </title>")
print ("<head>")
print ("<html>")
print ("<body>")
print ("<h2> Waardes : %s %s</h2> " % (first_value, second_value))
print ("</body>")
print ("</html>")