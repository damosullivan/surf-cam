from time import sleep

import cv2

class SurfCam(object):
    VIDEO_CAPTURE_ID = 0

    def __init__(self, frequency=10, ):
        self.frequency = frequency
        self.cam = cv2.VideoCapture(VIDEO_CAPTURE_ID)

    def run(self):

        # setup, verify credentials, log?

        try:
            while True:

                image_name = self.captureImage()

                # store image

                # compress image

                # upload image

                sleep(self.frequency)
            
        except KeyboardInterrupt:
            print("Killed!")
        finally:
            cv2.VideoCapture(self.VIDEO_CAPTURE_ID).release()

        # terminated

    def captureImage(self):
        name = "test"
        s, im = self.cam.read()
        cv2.imwrite("{}.jpeg".format(name), im)
        return name


    def verifyAWS(self):
        pass

    def verifyDirecotry(self):
        pass
