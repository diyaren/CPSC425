
# coding: utf-8

# In[29]:


import numpy as np
import math
from scipy import signal
import matplotlib.pyplot as plt

def gauss1d(sigma):
    len = round(6*sigma)
    if len%2==0:
        len = len+1
    else:
        len = len
       
    initArr = np.arange(-(int)(len/2),(int)(len/2+1))
    initArr = (1/(2*math.pi*math.pow(sigma,2)))*(np.exp(-np.power(initArr,2)/(2*math.pow(sigma,2))))
    sumArr = np.sum(initArr)
    result = initArr/sumArr
    return result

def gauss2d(sigma):
    #get the 1D Gaussian
    gau1d = gauss1d(sigma)
    #convert 1D array into a 2D array
    gau1d = gau1d[np.newaxis]
    #get the transpose of the 2D array
    gauTrans = np.transpose(gau1d)
    #convolve two 2D arrays generate above 
    ans = signal.convolve2d(gau1d,gauTrans)
    print "result for ",sigma," is:"
    return ans
#tests
print gauss2d(0.5)
print gauss2d(1)
    

