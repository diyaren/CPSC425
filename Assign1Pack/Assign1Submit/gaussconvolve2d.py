
# coding: utf-8

# In[12]:


from PIL import Image
import numpy as np
import math
from scipy import signal


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
    gau1d = gauss1d(sigma)
    gau1d = gau1d[np.newaxis]
    gauTrans = np.transpose(gau1d)
    ans = signal.convolve2d(gau1d,gauTrans)
    print "result for ",sigma," is:"
    return ans

def gaussconvolve2d(array,sigma):
    gau2d = gauss2d(sigma)
    #applied Gaussian convolution to a 2D array for the given value of sigma
    ans = signal.convolve2d(array,gau2d,'same')
    return ans

#open and load the image
img = Image.open("/Users/diyaren/Desktop/CPSC425/Assignments/Assign1/dog.jpg")
img.load()
#copy the initial pic
initImg = img
#convert the RGB pic into greyscale
img = img.convert("L")
#save the greyscale pic
img.save("greyscale.png")
#convert the greyscale pic into Numpy array
numpyArr = np.asarray(img)
#apply Gaussian filter with sigma 3
filter_Image_Array = gaussconvolve2d(numpyArr,3)
#set data type to unit8 for 8 bit image
filter_Image_Array = filter_Image_Array.astype('uint8')
#convert from numpy array to image
filteredImage = Image.fromarray(filter_Image_Array)
#get the filtered image
filteredImage.save("filteredDog.png") 
#open images on screen
initImg.show()
img.show()
filteredImage.show()

