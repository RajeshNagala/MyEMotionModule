from imutils.video import VideoStream
from imutils import face_utils
import argparse
import datetime
import imutils
import time
import dlib
import cv2
import threading

global vs

def main():    
    ap = argparse.ArgumentParser()

    ap.add_argument("-p","--shape-predictor", required=True,
        help="Path to facial landmark predictor")

    ap.add_argument("-r","--camera",type=int,default=1,
        help="whether to use picamera or not")

    args = vars(ap.parse_args())
    print args
    runtheshow(args)

def getdetecnpredict(args):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])
    return detector, predictor

def getVideoStream(args):
    print "Camera is getting warming up, pls wait"
    vs = VideoStream(usePiCamera=args["camera"] > 0).start()
    time.sleep(2.0)
    return vs

def detectface(gray):
    print "face detected"
    rects = detector(gray,0)

def runtheshow(args):
    while True:
        vs = getVideoStream(args)
        frame = vs.read()
        frame = imutils.resize(frame,width=400)
    
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        t = threading.Thread(name="detectface",target=detectface,args=gray)
        t.daemon=True
        t.start()
        
    
        for rect in rects:
            shape = predictor(gray,rect)
            shape = face_utils.shape_to_np(shape)

            for (x,y) in shape:
                cv2.circle(frame,(x,y),1,(0,0,255),1)
        
        cv2.imshow("frame",frame)
        key = cv2.waitKey(1) & 0xFF
    
        if key == ord("q"):
            break

    cv2.detroyAllWindows()
    vs.stop()

if __name__ == "__main__":
    e = threading.Event()
    t1 = threading.Thread
    main();
