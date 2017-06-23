from imutils.video import VideoStream
from imutils import face_utils
import MyWebPiCam
import argparse
import datetime
import imutils
import time
import dlib
import cv2
import threading

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

vs = VideoStream(usePiCamera=args["camera"]>0).start()
time.sleep(2.0)

global frame

"""
class myclass:
    def __init__(self):
        self.vs = VideoStream(True).start()
        time.sleep(10.0)
        print "initialize"
    
    def start(self):
        t = threading.Thread(target=self.update,args=())
        t.daemon = True
        t.start()
        print "start class"
        return self
    
    def update(self):
        print "read Frame",self.vs.read()
        self.frame = self.vs.read()
    
    def getframe(self):
        return self.frame
#frame=None


mstream = myclass().start()
"""

def displayupdate(cv2,frame):
    #print "display"
    frame = imutils.resize(frame, width=400)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    rects = detector(gray,0)
    
    for rect in rects:
        shape = predictor(gray,rect)
        shape = face_utils.shape_to_np(shape)

        for (x,y) in shape:
            cv2.circle(frame,(x,y),1,(0,0,255),1)
        
    cv2.imshow("frame",frame)
    
#frame = vs.read()
#t = threading.Thread(target=displayupdate,args=(cv2,frame))
#t.start()
count = 0
while True:
    # threading.Thread(name="frameThread",target=getFrame(),args=vs).start()
    count += 1
    st = count % 30
    if st == 0:
        frame = vs.read()
        displayupdate(cv2,frame)
        #frame = mstream.getframe()
        #t.start()
        """
        frame = imutils.resize(frame, width=400)

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
        rects = detector(gray,0)
    
        for rect in rects:
            shape = predictor(gray,rect)
            shape = face_utils.shape_to_np(shape)

            for (x,y) in shape:
                cv2.circle(frame,(x,y),1,(0,0,255),1)
        
        cv2.imshow("frame",frame)
        """
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

cv2.detroyAllWindows()
vs.stop()
