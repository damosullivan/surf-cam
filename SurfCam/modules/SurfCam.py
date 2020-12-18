import time
import cv2
import os
import boto3
import tempfile
import imutils
import os

from PIL import Image


VIDEO_CAPTURE_ID = 0
BUCKET = "farranahown-com"

class SurfCam(object):

    def __init__(self, frequency=1):
        self.frequency = frequency
        
        self.s3_client = boto3.client('s3',
            endpoint_url='https://s3.us-west-000.backblazeb2.com',
            aws_access_key_id=os.environ.get('BACKBLAZE_KEY_ID'),
            aws_secret_access_key=os.environ.get('BACKBLAZE_APPLICATION_KEY'))

        self.cam = cv2.VideoCapture(VIDEO_CAPTURE_ID)
        
        self.image_directory = tempfile.mkdtemp()

    def run(self):

        while True:

            try:

                image_name = self.captureImage()

                print("Processing: {}".format(image_name))

                compressed_image = self.compressImage(image_name)

                self.uploadImageToS3(compressed_image)
                self.updateLatestTracker(compressed_image)

                self.deleteFile(image_name)
                self.deleteFile(compressed_image)

                time.sleep(self.frequency)

            except Exception as e:

                # Basic error handling to stop crashing
                
                print(e)
                time.sleep(20)
            
    def captureImage(self):
        filename = "{}.png".format(str(time.time()).split('.')[0])
        file_path = self.getAbsoluteTempPath(filename)
        _, image = self.cam.read()
        image = imutils.resize(image, width=800)
        cv2.imwrite(file_path, image)
        
        return filename

    def uploadImageToS3(self, filename):
        file_path = self.getAbsoluteTempPath(filename)
        self.s3_client.upload_file(file_path, BUCKET, filename, ExtraArgs={'ACL':'public-read', "ContentType": "image/jpeg"})

    def updateLatestTracker(self, latest):
        key = "latest"
        self.s3_client.put_object(Bucket=BUCKET, Key=key, ACL='public-read', Body=latest, ContentType='text/plain')

    def deleteFileOnS3(self, filename):
        file_path = self.getAbsoluteTempPath(filename)
        self.s3_client.delete_object(Bucket=BUCKET, Key=filename)

    def deleteFile(self, filename):
        file_path = os.path.join(self.image_directory, filename)
        os.remove(file_path)

    def getAbsoluteTempPath(self, filename):
        return os.path.join(self.image_directory, filename)

    def compressImage(self, filename):
        infile = self.getAbsoluteTempPath(filename)
        outfile = self.getAbsoluteTempPath(filename.split('.')[0]) + '.jpeg'
        with Image.open(infile) as im:
            # im = im.resize((800, 600),Image.LANCZOS)
            im.save(outfile, "jpeg", quality=90, optimize=True)

        return os.path.basename(outfile)

    def verifyFilePermissions(self):
        filename = "connection.txt"
        with open(self.getAbsoluteTempPath(filename), 'w') as f:
            f.write("Verifying required S3 access")

        self.uploadImageToS3(filename)
        self.deleteFileOnS3(filename)
        self.deleteFile(filename)

        print("Verify: Has local file and S3 access")

    def verifyCameraPermissions(self):
        filename = self.captureImage()
        if os.path.exists(self.getAbsoluteTempPath(filename)):
            self.deleteFile(filename)
        else: 
            raise Exception("Image from camera not found")

        print("Verify: Has camera access")

    def teardown(self):
        cv2.VideoCapture(VIDEO_CAPTURE_ID).release()
