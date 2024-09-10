import cv2
import numpy as np
import pyautogui
from recorder import Recorder
from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/best.pt')
recorder = Recorder()

cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

cv2.resizeWindow("Live", 640, 640)

confidence_threshold = 0.70
while True:
    image = pyautogui.screenshot()
 
    results = model(image)

    for result in results:
        boxes = result.boxes
        confs = boxes.conf.cpu().numpy()
        filtered_boxes = boxes[confs > confidence_threshold]
        if len(filtered_boxes) > 0:
            result.boxes = filtered_boxes
            rendered_image = result.plot()
        else:
            rendered_image = image

    rendered_np = np.array(rendered_image)
 
    recorder.recording.write(rendered_np)
 
    rendered_np = cv2.cvtColor(rendered_np, cv2.COLOR_BGR2RGB)
     
    cv2.imshow('Live', rendered_np)
     
    if cv2.waitKey(1) == ord('q'):
        break

recorder.recording.release()
cv2.destroyAllWindows()