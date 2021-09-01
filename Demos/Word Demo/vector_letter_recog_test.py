# from keras.models import load_model
# from keras.models import model_from_json

from os import wait
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import time

import cv2
import numpy as np
from matplotlib import pyplot as plt


import anki_vector as av
from anki_vector.events import Events
from anki_vector.util import degrees, Pose
from anki_vector.connection import ControlPriorityLevel
from anki_vector.messaging import behavior_pb2
from anki_vector.messaging.shared_pb2 import Event

def Load_Model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('model.h5')
    model = loaded_model
    print('Model successfully loaded')
    return model

    
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


def use_model(model,img):
    pred = model.predict_classes(img)
    return pred


class Letter_Bounding_box():
    def __init__(self):
        self.x1,self.y1,self.x2,self.y2 = 0,0,0,0

def Handle(robot, event_type,event,Box):
    Box.x1,Box.y1 = int(event.image_rect.x_top_left+event.image_rect.width/5),int(event.image_rect.y_top_left-event.image_rect.height/2)
    Box.x2,Box.y2 = int(Box.x1+event.image_rect.width/1.25),int(event.image_rect.y_top_left+event.image_rect.height/4)

    
# def hardcoded_check(roi):



def main(args = None):
    characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    model = Load_Model()
    # img = cv2.imread('A.jpg')

    BB = Letter_Bounding_box()
    robot = av.AsyncRobot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(0.0))
    robot.camera.init_camera_feed()
    robot.events.subscribe(Handle, Events.object_observed,BB)

    time.sleep(5)

    t0 = time.time()
    # while time.time()-t0 < 60:
    while True:
        cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        if BB.x2-BB.x1 > 0 and BB.y2-BB.y1 >0:
            roi = cv_image[BB.y1:BB.y2,BB.x1:BB.x2]
            if roi is not None:
                try:
                    rois, imgs = get_rois(roi)
                except:
                    print("E")
            for i in range(len(rois)):
                processed_img = rois[i]
                img = imgs[i]
                pred = use_model(model,processed_img)
                character_guess = characters[pred[0]]
                print("Predicted character = {}".format(character_guess))
                # print("Confidence = {}".format(pred[0]))
                # cv2.imshow("{}, area = {}".format(character_guess, img.shape[0]*img.shape[1],img.shape),img)
        
        time.sleep(1)
        # cv2.waitKey(0)
        # input("next?")
        # cv2.destroyAllWindows()

    
if __name__ == '__main__':
    main()