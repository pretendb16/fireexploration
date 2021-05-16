# Source: https://www.youtube.com/watch?v=qOyDrR3h5uI&t=548s
# Source: https://github.com/mkleehammer/pyodbc/wiki/Getting-started
# cd /e/'fire research'/'04262021 fire data analysis'

import pyodbc

con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\fire research\04262021 fire data analysis\FPA_FOD_20170508.accdb;'
conn = pyodbc.connect(con_string)

cur=conn.cursor()


# find the years of fire occurance data

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


# get fire occurance data
CA_firecount_list=[]
for i in years:
    cur.execute("SELECT fire_year FROM Fires WHERE state ='CA' AND fire_year=?",(i))
    CA_firedata = cur.fetchall()
    CA_firecount=len(CA_firedata)
    CA_firecount_list+=[CA_firecount]
print(CA_firecount_list)

# fire size in California data
# source: https://www.fire.ca.gov/media/11397/fires-acres-all-agencies-thru-2018.pdf

fire_size_year_range=[1987,2018]
fire_size_year=np.arange(fire_size_year_range[0],fire_size_year_range[1]+1,1)
fire_size_year= fire_size_year.tolist()
print(fire_size_year)

fire_size_data=[873000,345000,173400,365200,44200,282745,309779,526219,209815,752372,283885,

215412,1172850,295026,377340,538216,965770,311024,279214,863345,1520362,1593690,451969,134462,

228599,829224,601635,625540,880899,669534,1548429,1975086]



# plotting

import matplotlib.pyplot as plt

xpoints = np.array(years)
ypoints = np.array(CA_firecount_list)
xpoints_size=np.array(fire_size_year)
ypoints_size=np.array(fire_size_data)



# source: https://www.kite.com/python/answers/how-to-plot-two-series-with-different-scales-in-python
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()

lns1=ax_left.plot(xpoints, ypoints,'-r',label='Fire Occurance')
lns2=ax_right.plot(xpoints_size,ypoints_size,'-g',label='Wildfire Burn Area')

plt.title('Trend of Wildfire Occurance and Burn Area \n in California from '+str(fire_size_year_range[0])+' to '+str(fire_size_year_range[1]))
ax_left.set_xlabel('Year')
ax_left.set_ylabel('# of Fire Occurance in California')
ax_right.set_ylabel('California Wildfire Burn Area (acres)')

lns=lns1+lns2
labs=[l.get_label() for l in lns]
ax_left.legend(lns,labs,loc='upper center')

plt.show()
