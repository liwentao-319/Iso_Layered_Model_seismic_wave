from obspy import read 
import matplotlib.pyplot as plt 
import matplotlib as mpl
from glob import glob 
import numpy as np 
filenames = sorted(glob("observed_T01/*R.SAC"))
pretime = 5
dt = 0.01
datas=[]
ray_params=[]
for filename in filenames:
    st= read(filename)
    tr=st[0]
    ray_params.append(tr.stats.sac['user0'])
    data=tr.data
    datas.append(data)
fig=plt.figure(figsize=(8,5))
ax=fig.add_subplot()

hah=zip(ray_params,datas)
hah = sorted(hah,key=lambda x:x[0])
ray_params,datas = zip(*hah)
ray_params=np.array(ray_params)
norm = plt.Normalize(ray_params.min(),ray_params.max())
cmap = mpl.cm.ScalarMappable(norm=norm,cmap='cool')
xtime = np.arange(len(datas[0]))*dt-pretime
for i,data in enumerate(datas):
    ray_p = ray_params[i]
    print(ray_p)
    line=ax.plot(xtime,data,lw=0.3,color=cmap.to_rgba(ray_p),label='ray_p:{0:5.4f}'.format(ray_p))
ax.set_xlabel("time[s]")
ax.set_ylabel("amp")
ax.set_title("R with different ray_parameter")

ax.legend(loc='upper right')
plt.show()
