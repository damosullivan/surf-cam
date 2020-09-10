import time
import cv2
import os
import boto3
import tempfile

VIDEO_CAPTURE_ID = 0
BUCKET = "farranahown"

class SurfCam(object):

    def __init__(self, frequency=10):
        self.frequency = frequency
        self.image_directory = tempfile.mkdtemp()

        print("boto")
        
        self.s3_client = boto3.client('s3')

        print("cam")

        self.cam = cv2.VideoCapture(VIDEO_CAPTURE_ID)

        print("init")

    def run(self):

        # setup, verify credentials, log?
        print("start")

        # try:
        # while True:

        print("go")
        image_name = self.captureImage()
        # self.uploadImage(image_name)

        # store image

        # compress image

        # upload image

        time.sleep(self.frequency)
            
        # except KeyboardInterrupt:
        #     print("Killed!")
        # finally:
        #     cv2.VideoCapture(VIDEO_CAPTURE_ID).release()

        # terminated

    def captureImage(self):
        filename = "{}.jpeg".format(str(time.time()).split('.')[0])
        file_path = os.path.join(self.image_directory, filename)
        s, image = self.cam.read()
        cv2.imwrite(file_path, image)

        print("Captured: {}".format(file_path))
        
        return filename

    def uploadImage(self, filename):
        file_path = os.path.join(self.image_directory, filename)
        self.s3_client.upload_file(file_path, BUCKET, filename)

        print("Uploaded: {}".format(filename))


    def verifyAWS(self):
        pass

    def verifyDirecotry(self):
        pass
