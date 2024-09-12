import cv2
import numpy as np

def plane_detector(model, image, confidence_threshold):
    """
    Detects the planes and returns the image with bounding boxes
    around the planes that meet the confidence threshold.
    
    If no planes within the confidence threshhold are detected,
    the original image is returned.
    
    Parameter model: the YOLO model
    Precondition: a YOLO model object that has been trained
    
    Parameter image: image of the frame from the video
    Precondition: a pyautogui image object

    Parameter confidence_threshold: What confidence threshold the
    the detection must meet for the bounding box to appear
    Precondition: a float between 0.00 and 1.00
    """

    image = cv2.resize(image, (640, 640))
    # Run frame through the model
    results = model(image)

    for result in results:
        boxes = result.boxes
        confs = boxes.conf.cpu().numpy()
        # Filters out bounding boxes below threshold
        filtered_boxes = boxes[confs > confidence_threshold]
        # If any boxes meet the threshold, plot them
        if len(filtered_boxes) > 0:
            result.boxes = filtered_boxes
            rendered_image = result.plot(labels=False, conf=False)
        else:
            rendered_image = image
    rendered_image = cv2.resize(rendered_image, (256, 256))
    return np.array(rendered_image), len(filtered_boxes)