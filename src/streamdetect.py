import cv2
import pyautogui
from recorder import Recorder
from planedetector import plane_detector
from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/best.pt')
recorder = Recorder()

while True:
    image = pyautogui.screenshot()
 
    rendered_np = plane_detector(model, image, confidence_threshold = 0.60)

    recorder.recording.write(rendered_np)
     
    cv2.imshow('Live', rendered_np)
     
    if cv2.waitKey(1) == ord('q'):
        break

recorder.recording.release()
cv2.destroyAllWindows()