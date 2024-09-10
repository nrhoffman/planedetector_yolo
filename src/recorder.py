import cv2
import pyautogui

class Recorder():
    def __init__(self):
        resolution = self.GetResolution()
        fps = 30.0
        codec = cv2.VideoWriter_fourcc(*"XVID")
        filename = "Recording.avi"
        self.recording = cv2.VideoWriter(filename, codec, fps, resolution)
    
    def GetResolution(self):
        res = pyautogui.size()
        return (res.width, res.height)