# Source: https://www.youtube.com/watch?v=qOyDrR3h5uI&t=548s
# Source: https://github.com/mkleehammer/pyodbc/wiki/Getting-started
# cd /e/'fire research'/'04262021 fire data analysis'

import pyodbc

con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\fire research\04262021 fire data analysis\FPA_FOD_20170508.accdb;'
conn = pyodbc.connect(con_string)

cur=conn.cursor()

# This is just an example that works for PostgreSQL and MySQL, with Python 2.7.
conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
conn.setencoding(encoding='utf-8')

# find the years

cur.execute('SELECT fire_year FROM Fires')
initial_year_value = cur.fetchone()
earliest_year=initial_year_value
latest_year=initial_year_value

cur.execute('SELECT fire_year FROM Fires')
for year_num in cur.fetchall():
    if year_num>latest_year:
        latest_year=year_num
    elif year_num<earliest_year:
        earliest_year=year_num
print('The earliest year of fire data is '+str(earliest_year[0])+'.')
print('The latest year of fire data is '+str(latest_year[0])+'.')

# create x axis for years
import numpy as np

years=np.arange(earliest_year[0],latest_year[0]+1,1)
years= years.tolist()
print(years)


# get fire data
CA_firecount_list=[]
for i in years:
    cur.execute("SELECT fire_year FROM Fires WHERE state ='CA' AND fire_year=?",(i))
    CA_firedata = cur.fetchall()
    CA_firecount=len(CA_firedata)
    CA_firecount_list+=[CA_firecount]
print(CA_firecount_list)

# plotting

import matplotlib.pyplot as plt

xpoints = np.array(years)
ypoints = np.array(CA_firecount_list)

plt.plot(xpoints, ypoints,'D-g',mec='r',mfc='r')
plt.title('Trend of Fire Occurance in California from '+str(earliest_year[0])+' to '+str(latest_year[0]))
plt.xlabel('Year')
plt.ylabel('# of Fire Occurance in California')
plt.show()
