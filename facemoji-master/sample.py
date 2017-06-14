# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('faces.xml')
eyes_cascade = cv2.CascadeClassifier('eyes.xml')
nose_cascade = cv2.CascadeClassifier('nose.xml')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
    print "Found {0} face".format(len(faces))

    for (x, y, w, h) in faces:
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = image[y:y+h,x:x+w]
        eyes = eyes_cascade.detectMultiScale(roi_gray)
        nose = nose_cascade.detectMultiScale(roi_gray)
        # if nose:
        #     print "Nose found"
        # if eyes:
        #     print "Eyes found"
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),1)
        for (nx,ny,nw,nh) in nose:
            cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(0,255,255),1)

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
