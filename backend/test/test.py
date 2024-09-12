import cv2
import torch
from numpy import asarray
from ultralytics import YOLO

image = cv2.imread('../images/planes_example_1.png')
cv2.resize(image, (640,640))

model = YOLO('../src/runs/detect/train/weights/best.pt')

results = model(image)

for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")