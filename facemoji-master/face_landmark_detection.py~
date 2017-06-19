from imutils import face_utils
import numpy as np
import dlib
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()

ap.add_argument("-p","--shape_predictor", required=True,
    help="Path to facial landmark predictor")

ap.add_argument("-i","--image",required=True,
    help="path to input image")
    
args = vars(ap.parse_args())

print args

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

image = cv2.imread(args["image"])
image = imutils.resize(image,width=500)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

rects = detector(gray,1)


for (i,rect) in enumerate(rects):
    print "face is at",rect
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    (x,y,w,h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    
    cv2.putText(image,"face {}".format(i+1),(x-10,y-10),
        cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    
    #k = 0
    for (x,y) in shape:
        """"
        k += 1
        #getting the eye coordinates
        if k > 36 and k < 49:
            print k
            cv2.circle(image,(x,y),1,(190,38,255),1)
        """
        cv2.circle(image,(x,y),1,(190,38,255),1)
cv2.imshow("output",image)
cv2.waitKey(0)