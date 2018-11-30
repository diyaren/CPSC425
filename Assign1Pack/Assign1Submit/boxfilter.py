
# coding: utf-8

# In[14]:


import numpy as np

def boxfilter(n):
    #assertion statement for which n is not odd
    assert n%2!=0,"Dimension must be odd" 
    #full n*n array with 0.04
    box = np.full((n,n),0.04)
    #sum up every element in the array
    sum = np.sum(box)
    #use the ratio of 0.04 and sum of the array elements 
    #as the new array numer
    result = box/sum
    return result

#tests
print boxfilter(3)
print boxfilter(5)
print boxfilter(4)

    

