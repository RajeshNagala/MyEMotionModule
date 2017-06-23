import cv2
#from imutils.video import WebcamVideoStream
from imutils.video import VideoStream
from threading import Thread
import time

class mywebpi():
    def __init__(self, src=1):
        # initialize the video camera stream and read the first frame
        # from the stream
        # making sure that piCam is the default camera
        self.stream = VideoStream(True).start()
        time.sleep(2.0)
        print "just check",self.stream.read()
        self.frame = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            self.frame = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True