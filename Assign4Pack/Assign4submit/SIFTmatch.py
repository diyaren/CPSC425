from PIL import Image, ImageDraw
import numpy as np
import csv
import math
import random

def ReadKeys(image):
    """Input an image and its associated SIFT keypoints.

    The argument image is the image file name (without an extension).
    The image is read from the PGM format file image.pgm and the
    keypoints are read from the file image.key.

    ReadKeys returns the following 3 arguments:

    image: the image (in PIL 'RGB' format)

    keypoints: K-by-4 array, in which each row has the 4 values specifying
    a keypoint (row, column, scale, orientation).  The orientation
    is in the range [-PI, PI] radians.

    descriptors: a K-by-128 array, where each row gives a descriptor
    for one of the K keypoints.  The descriptor is a 1D array of 128
    values with unit length.
    """
    im = Image.open(image+'.pgm').convert('RGB')
    keypoints = []
    descriptors = []
    first = True
    with open(image+'.key','rb') as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC,skipinitialspace = True)
        descriptor = []
        for row in reader:
            if len(row) == 2:
                assert first, "Invalid keypoint file header."
                assert row[1] == 128, "Invalid keypoint descriptor length in header (should be 128)."
                count = row[0]
                first = False
            if len(row) == 4:
                keypoints.append(np.array(row))
            if len(row) == 20:
                descriptor += row
            if len(row) == 8:
                descriptor += row
                assert len(descriptor) == 128, "Keypoint descriptor length invalid (should be 128)."
                #normalize the key to unit length
                descriptor = np.array(descriptor)
                descriptor = descriptor / math.sqrt(np.sum(np.power(descriptor,2)))
                descriptors.append(descriptor)
                descriptor = []
    assert len(keypoints) == count, "Incorrect total number of keypoints read."
    print "Number of keypoints read:", int(count)
    return [im,keypoints,descriptors]

def AppendImages(im1, im2):
    """Create a new image that appends two images side-by-side.

    The arguments, im1 and im2, are PIL images of type RGB
    """
    im1cols, im1rows = im1.size
    im2cols, im2rows = im2.size
    im3 = Image.new('RGB', (im1cols+im2cols, max(im1rows,im2rows)))
    im3.paste(im1,(0,0))
    im3.paste(im2,(im1cols,0))
    return im3

def DisplayMatches(im1, im2, matched_pairs):
    """Display matches on a new image with the two input images placed side by side.

    Arguments:
     im1           1st image (in PIL 'RGB' format)
     im2           2nd image (in PIL 'RGB' format)
     matched_pairs list of matching keypoints, im1 to im2

    Displays and returns a newly created image (in PIL 'RGB' format)
    """
    im3 = AppendImages(im1,im2)
    offset = im1.size[0]
    draw = ImageDraw.Draw(im3)
    for match in matched_pairs:
        draw.line((match[0][1], match[0][0], offset+match[1][1], match[1][0]),fill="red",width=2)
    im3.show()
    return im3

def match(image1,image2):
    im1, keypoints1, descriptors1 = ReadKeys(image1)
    im2, keypoints2, descriptors2 = ReadKeys(image2)
    #Generate five random matches (for testing purposes)
    matched_pairs = []
    #performed SIFT
    #set the threshold
    ratio = 0.65
    #for each descriotor in the second image, find the best match point
    for kp2, dt2 in zip(keypoints2,descriptors2):
        angles = []
        #loop through each of the points and descriptor in image 1
        for kp1,dt1 in zip(keypoints1,descriptors1):
            #calculate the dot product
            dotproducts = np.array(dt1) * np.array(dt2)
            #compute the inverse consine of the dot product of the vectors
            inversecos  = math.acos(np.sum(dotproducts))
            angles.append(inversecos);
        #sorted angles array and try to find the smallest and the second smallest angles
        sortedarr = sorted(angles)
        var1 = sortedarr[0]
        var2 = sortedarr[1]

        #check if the ration of the two angles chosen smaller than threshold
        if var1/var2 < ratio:
            #save the two angles if the ratio less then threshold
            kp1 = keypoints1[angles.index(var1)]
            matched_pairs.append([kp1,kp2])

    #performed RANSAC
    selecttimes = 10
    twopi = 2 * math.pi 
    #set the threshold as radians 
    orientthreshold = math.pi*30/180
    scalthreshold = 0.1
    inlierlist = []
    #random selection 10 times and then select the largest 
    #consistent subset that was found
    for i in range(selecttimes):
        [k1,k2] = matched_pairs[random.randrange(len(matched_pairs))];
        matchlist = []
        #calculate the orientation and scale diff for random seleted match 
        orientdiff1 = abs(k1[3]-k2[3]) % twopi
        scalediff1  = k1[2]/k2[2]
        #check all the other matches for consistency
        for [comparek1,comparek2] in matched_pairs:
            #compute the orientation and scale diff for second match
            orientdiff2 = abs(comparek2[3]-comparek1[3]) % twopi
            scalediff2  = comparek1[2]/comparek2[2]
            #compute the orientation and scale diff these two matches diff
            orientdiff = abs(orientdiff1 - orientdiff2) % twopi
            scalediff  = abs(scalediff1 - scalediff2)
            #save the consistent pair if the threshold conditions are satisfied
            if orientdiff< orientthreshold and scalediff < scalthreshold:
                matchlist.append([comparek1,comparek2])
            #if the consistent list is larger than the inlier list, save it as the new inlierlist
            if len(inlierlist) < len(matchlist) :
                inlierlist = matchlist



    #
    # END OF SECTION OF CODE TO REPLACE
    #
    im3 = DisplayMatches(im1, im2,inlierlist)
    return im3

#Test run...
match('library2','library')
#match('scene','basmati')

