
class SurfCam:

    CAMERA_IDENTIFIER = 1

    def __init__(self, frequency: int, directory: str):
        self._frequency = frequency
        self._directory = directory

    def capture(self):
        print("capturing")