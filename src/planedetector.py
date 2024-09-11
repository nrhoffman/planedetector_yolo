import numpy as np

def PlaneDetector(model, image, confidence_threshold):
    results = model(image)

    for result in results:
        boxes = result.boxes
        confs = boxes.conf.cpu().numpy()
        filtered_boxes = boxes[confs > confidence_threshold]
        if len(filtered_boxes) > 0:
            result.boxes = filtered_boxes
            rendered_image = result.plot(labels=False, conf=False)
        else:
            rendered_image = image

    return np.array(rendered_image)