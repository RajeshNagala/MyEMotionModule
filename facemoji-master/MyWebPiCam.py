import cv2
from imutils.video import WebcamVideoStream
from imutils.video import VideoStream
from threading import Thread

class mywebpi(WebcamVideoStream):
    def __init__(self, src=1):
        # initialize the video camera stream and read the first frame
        # from the stream
        # making sure that piCam is the default camera
        self.stream = VideoStream(src > 0).start()
        (self.grabbed, self.frame) = self.stream.read()

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
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True