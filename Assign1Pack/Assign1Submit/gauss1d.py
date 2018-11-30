
# coding: utf-8

# In[28]:


import numpy as np 
import math

def gauss1d(sigma):
    #get length of the array
    len = round(6*sigma)
    if len%2==0:
        len = len+1
    else:
        len = len
    
    #set the arrage of the array base on the size limit     
    initArr = np.arange(-(int)(len/2),(int)(len/2+1))
    #get Guassian value bases on the formula
    initArr = (1/(2*math.pi*math.pow(sigma,2)))*(np.exp(-np.power(initArr,2)/(2*math.pow(sigma,2))))
    sumArr = np.sum(initArr)
    #normalization
    result = initArr/sumArr
    return result
#tests
print gauss1d(0.3)
print gauss1d(0.5)
print gauss1d(1)
print gauss1d(2)

