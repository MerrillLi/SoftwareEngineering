import datetime
import os
time='2019-12-05T15:23:00.002Z'
time=time.split('T')
time0=time[0]
print(time0)
time1=time[1]
time2=time1.split('.')
time2=time2[0]
time=time0+' '+time2
print(time)