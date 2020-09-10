import os
import argparse

from modules.SurfCam import SurfCam

if __name__ == '__main__':
    print("starting program")
    parser = argparse.ArgumentParser(description='Find nearby customers')
    # parser.add_argument('--input', '-c', help="file containing a JSON list of customers", default="customers.txt")
    # parser.add_argument('--distance', '-d', help="the customer radius catchment (km)", type=int, default="100")
    
    # args = parser.parse_args()

    # if not os.path.exists(args.input):
        # raise FileNotFoundError


    surf_cam = SurfCam()
    surf_cam.run()

    
    print("done")