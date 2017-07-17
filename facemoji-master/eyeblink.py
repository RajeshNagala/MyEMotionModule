from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

EYE_AR_THRES = 0.3
EYE_AR_CONSEC_FRAMES = 10

COUNTER = 0
TOTAL = 0
ALARM_ON = False


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1],eye[5])
    B = dist.euclidean(eye[2],eye[4])
    
    C = dist.euclidean(eye[0],eye[3])
    
    ear = (A + B)/(2.0 * C)
    
    return ear

ap = argparse.ArgumentParser()

ap.add_argument("-p","--shape-predictor", required=True,
    help="Path to facial landmark predictor")

ap.add_argument("-r","--camera",type=int,default=1,
    help="whether to use picamera or not")

args = vars(ap.parse_args())
print args

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

print "Camera is getting warming up, pls wait"
vs = VideoStream(usePiCamera=args["camera"] > 0).start()
time.sleep(2.0)

(lstart,lend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rstart,rend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

while True:
    frame = vs.read()
    frame = imutils.resize(frame,width=400)
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    rects = detector(gray,0)
    
    for rect in rects:
        shape = predictor(gray,rect)
        shape = face_utils.shape_to_np(shape)
        
        leftEye = shape[lstart:lend]
        rightEye = shape[rstart:rend]
        
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        
        ear = (leftEAR + rightEAR)/2.0
        
        # leftEyeHull = cv2.convexHull(leftEye)
        # rightEyeHull = cv2.convexHull(rightEye)
        
        # cv2.drawContours(frame,[leftEyeHull],-1,(255,0,0),1)
        # cv2.drawContours(frame,[rightEyeHull],-1,(255,0,0),1)
        print ear
        if ear < EYE_AR_THRES:
            COUNTER +=1
            print COUNTER
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True
                    """
                    if args["alarm"] != "": 
                        t = Thread(target=sound_alarm,args=(args["alarm"],))
                        t.daemon = True
                        t.start()
                    """
                print "Drowsiness alert"

                """
                cv2.putText(frame,"Drowsiness alert",(10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                """    
        else:
            COUNTER = 0
            ALARM_ON = False
        """
          This logic for eyeblink
        else:
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL += 1
                print "Blink {0}".format(TOTAL)
                
            COUNTER = 0

        cv2.putText(frame,"Blink: {}".format(TOTAL),(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        
        cv2.putText(frame,"EAR: {:.2f}".format(ear),(300,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        """
    cv2.imshow("frame",frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()

