import cv2
import pyautogui
from recorder import Recorder
from planedetector import PlaneDetector
from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/best.pt')
recorder = Recorder()
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Live", 640, 640)

confidence_threshold = 0.60
while True:
    image = pyautogui.screenshot()
 
    rendered_np = PlaneDetector(model, image, confidence_threshold)

    recorder.recording.write(rendered_np)
 
    rendered_np = cv2.cvtColor(rendered_np, cv2.COLOR_BGR2RGB)
     
    cv2.imshow('Live', rendered_np)
     
    if cv2.waitKey(1) == ord('q'):
        break

recorder.recording.release()
cv2.destroyAllWindows()