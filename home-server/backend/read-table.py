# TODO: pull from .css file for the styles in contents
# TODO: make the table generation happen more programmatically 
# read the tables in the mariadb and display in the webbrowser
import mariadb

conn = mariadb.connect(user='root', password='',host='localhost',database='hems')

if conn:
    print("Successfully connected to the database.")
else:
    print("Failed to connect to the database.")

#generate the html devices table
select_device = """SELECT * FROM devices"""
cursor = conn.cursor()
cursor.execute(select_device)
result = cursor.fetchall()

p = []

#table header
tbl = "<tr><td>ID</td><td>Name</td><td>Update</td></tr>"
p.append(tbl)
#devices table
for row in result:
    a="<tr><td>%s</td>"%row[0]
    p.append(a)
    b = "<td>%s</td>"%row[1]
    p.append(b)
    c = "<td>%s</td></tr>"%row[2]
    p.append(c)


#html contents:
contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
    <head>
        <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
        <title>Python Web Browser</title>
        <style>
        table, th, td{ border: 1px solid black;}
        </style>
    </head>
    <body>
        <table>
            %s
        </table>
    </body>
</html>
'''%(p)

# write to the html file
filename = '../html/index.html'

def main(contents, filename):
    output = open(filename,"w")
    output.write(contents)
    output.close()

main(contents, filename)
#webbrowser.open(filename)
