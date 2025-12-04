#%%
import numpy as np
import os.path as op
from LayerModel import rfmini
import os 
import matplotlib.pyplot as plt 
from time import time 
from obspy.io.sac.sactrace import SACTrace

mod_flnm='model_final_T01'
Thick, Vp, Vs, Rho = np.loadtxt(mod_flnm,unpack=True)
Thick=Thick.astype('float')
Vp = Vp.astype('float')
Vs = Vs.astype('float')
Rho = Rho.astype('float')

z = np.cumsum(Thick)
z = np.concatenate(([0], z[:-1]))
gauss=3.0
qa  = np.ones(Vp.shape)*50000000000
qb =  np.ones(Vp.shape)*25000000000
pretime = 5
Nt=5000
dt=0.01
nsv=0.
km2deg =1/180*np.pi*6378 
path = 'observed_T01'
if not os.path.isdir(path):
    os.makedirs(path)
nsvp, nsvs = float(Vp[0]), float(Vs[0])
vpvs = nsvp / nsvs
poisson = (2 - vpvs**2)/(2 - 2 * vpvs**2)

#%%
# receiver functions

header = {'kstnm': 'TEST', 'stla': 0.0, 'stlo': 0.,
          'evla': 0.0, 'evlo': 0.0, 'evdp': 50, 'nzyear': 2022,
          'nzjday': 57, 'nzhour': 13, 'nzmin': 43, 'nzsec': 17,
          'nzmsec': 100, 'delta': dt}
nray=10
ray_params=np.linspace(0.03,0.07,nray)
nsamp = 2.**int(np.ceil(np.log2(Nt * 2)))
for i in range(nray):
    filename="{0}/test_{1}.SAC".format(path,i+1)
    ray_param = ray_params[i]*km2deg
    zz,rr,rf,zrf = rfmini.synrf(z,Vp,Vs,Rho,qa,qb,ray_param,gauss,nsamp,1/dt,pretime,nsv,poisson,'P')
    sactracez = SACTrace(data=zz[:Nt],user0=ray_params[i],kcmpnm='TZ',**header)
    sactracez.write(filename.replace(".SAC",".Z.SAC"))
    sactracer = SACTrace(data=rr[:Nt],user0=ray_params[i],kcmpnm='TR',**header)
    sactracer.write(filename.replace(".SAC",".R.SAC"))
#    sactracerf = SACTrace(data=rf[:Nt],user0=ray_params[i],kcmpnm='TRF',**header)
#    sactracerf.write(filename.replace(".SAC",".RF.SAC"))
