import numpy as np
import time 

def cal_inv(msz):
  A=np.random.rand(msz**2).reshape((msz, msz))
  tl=time.time()
  Ainv=np.linalg.inv(A)
  dtl=time.time()-tl
  return dtl