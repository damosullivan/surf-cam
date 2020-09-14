import time
import cv2
import os
import boto3
import tempfile

from PIL import Image


VIDEO_CAPTURE_ID = 0
BUCKET = "farranahown"

class SurfCam(object):

    def __init__(self, frequency=10):
        self.frequency = frequency
        
        self.s3_client = boto3.client('s3')
        self.cam = cv2.VideoCapture(VIDEO_CAPTURE_ID)
        
        self.image_directory = tempfile.mkdtemp()

    def run(self):

        while True:

            image_name = self.captureImage()

            print("Processing: {}".format(image_name))

            compressed_image = self.compressImage(image_name)

            self.uploadFileToS3(compressed_image)

            self.deleteFile(image_name)
            self.deleteFile(compressed_image)

            time.sleep(self.frequency)
            
    def captureImage(self):
        filename = "{}.png".format(str(time.time()).split('.')[0])
        file_path = self.getAbsoluteTempPath(filename)
        s, image = self.cam.read()
        cv2.imwrite(file_path, image)
        
        return filename

    def uploadFileToS3(self, filename):
        file_path = self.getAbsoluteTempPath(filename)
        self.s3_client.upload_file(file_path, BUCKET, filename, ExtraArgs={'ACL':'public-read'})

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
            im = im.resize((800, 600),Image.LANCZOS)
            im.save(outfile, "jpeg", quality=25, optimize=True)

        return os.path.basename(outfile)

    def verifyFilePermissions(self):
        filename = "connection.txt"
        with open(self.getAbsoluteTempPath(filename), 'w') as f:
            f.write("Verifying required S3 access")

        self.uploadFileToS3(filename)
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
