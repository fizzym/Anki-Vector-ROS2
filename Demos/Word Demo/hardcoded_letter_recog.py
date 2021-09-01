import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_rois(image):
    height, width, depth = image.shape
    #resizing the image to find spaces better
    image = cv2.resize(image, dsize=(width*5,height*4), interpolation=cv2.INTER_CUBIC)
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #binary
    ret,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow("thresh",thresh)
    # cv2.waitKey(0)
    # #dilation
    # kernel = np.ones((5,5), np.uint8)
    # img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    # #adding GaussianBlur
    # gsblur=cv2.GaussianBlur(img_dilation,(5,5),0)
    #find contours
    # im2,ctrs, hier = cv2.findContours(gsblur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    m = list()
    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    pchl = list()
    dp = image.copy()

    # drw = cv2.drawContours(image,ctrs,-1,(255,0,0),2)
    # cv2.imshow("draw",drw)
    # cv2.waitKey(0)
    area_max = 0
    temp_roi = None
    rois = []
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
        # Getting ROI
        roi = image[y-10:y+h+10, x-10:x+w+10]
        shape = roi.shape
        area = shape[0]*shape[1]
        # print("Shape = {}".format(shape))
        if area>area_max:
            area_max = area
            temp_roi = roi

    # cv2.imshow("ROI",roi)
    # cv2.waitKey(0)
    # rois.append(roi)
    if temp_roi is not None:
        rois.append(temp_roi)
        roi = cv2.resize(temp_roi, dsize=(28,28), interpolation=cv2.INTER_CUBIC)
        roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        
        roi = np.array(roi)
        t = np.copy(roi)
        t = t / 255.0
        t = 1-t
        t = t.reshape(1,784)
        m.append(t)
    # cv2.destroyAllWindows()
    # input("Return length = {}".format(len(m)))
    
    return m, rois


def process_img(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
    return thresh

def identify_letter(img):
    thresh = process_img(img)
    plt.imshow(img)
    plt.show()
    
