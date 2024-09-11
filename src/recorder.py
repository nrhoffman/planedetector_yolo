import cv2
import pyautogui

class Recorder():
    """
    A class representing the cv2 window display

    Attributes:
        self.recording = the videowriter object
    """
    def __init__(self):
        """ Inits the class """
        resolution = self.getResolution()
        fps = 60.0
        codec = cv2.VideoWriter_fourcc(*"XVID")
        filename = "Recording.avi"
        self.recording = cv2.VideoWriter(filename, codec, fps, resolution)
    
    def getResolution(self):
        """ Gets the resolution of the active monitor and returns it"""
        res = pyautogui.size()
        return (res.width, res.height)