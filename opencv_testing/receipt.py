# USAGE
# python convert_winco_receipt.py --image images/page.jpg --scanned images/page_scanned.jpg

# import the necessary packages
from pyimagesearch.transform import four_point_transform
#from pyimagesearch import imutils
import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2

from PIL import Image
import pytesseract
import re

def winco_receipt_line(line):
    s = re.search(r'((I|T)F)|((I|T)x)', line)
    if(s is None):
        return None

    TF_ind = s.start()

    output_string = ', '.join((re.sub(r'\W+', '', line[0:20]), ' ',
        line[TF_ind-5:TF_ind].rstrip()))

    return output_string

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
ap.add_argument("-s", "--scanned", required = False, default='scanned', 
	help = "Where to save the scanned image")
ap.add_argument("-c", "--csv", required = False,
	help = "Where to save the scanned image")
ap.add_argument("-w", "--which_receipt", required = False, default='winco',
	help = "Where to save the scanned image")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
#image = cv2.imread('image.jpg')
print(image)
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# show the original image and the edge detected image
print "STEP 1: Edge Detection"
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
        print(len(approx))
	if len(approx) == 4:
		screenCnt = approx
		break

# show the contour (outline) of the piece of paper
print "STEP 2: Find contours of paper"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 250, offset = 10)
warped = warped.astype("uint8") * 255

# show the original and scanned images
print "STEP 3: Apply perspective transform"
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)
cv2.destroyAllWindows()

#Save transformed image
sp = args['image'].split('.')
save_filename = sp[0] + '_' + args['scanned'] + '.' + sp[1]
cv2.imwrite(save_filename, warped)

###
#Convert image to csv fie
###

# show the original and scanned images
print "STEP 4: Convert receipt to csv file"
csv_filename = sp[0] + '.csv'
csv_file = open(csv_filename, "w")

if(args['which_receipt'] == 'winco'):
    process_line = winco_receipt_line

st = pytesseract.image_to_string(Image.open(save_filename), config="-psm 6")
for cur_line in st.split('\n'):
    print(cur_line)
    ret = process_line(cur_line)

    if(ret is None):
        continue

    csv_file.write(ret + '\n')

csv_file.close()

