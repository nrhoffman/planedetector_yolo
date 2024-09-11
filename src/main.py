import cv2
import numpy as np
from dotenv import load_dotenv
from imageprocessing import ImageProcessing
from tilecreator import TileCreator

load_dotenv()

tilecreator = TileCreator(39.07186599114265, -84.68659910621555, 39.024939242268246, -84.64273962440403)

stitched_image_ratio, stitched_image = ImageProcessing(tilecreator)

cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
if stitched_image_ratio >= 1.00:
    width = 1080
    height = int(1080 / stitched_image_ratio)
else:
    width = int(1080 * stitched_image_ratio)
    height = 1080

cv2.resizeWindow("Live", width, height)

cv2.imshow('Live', np.array(stitched_image))
cv2.waitKey(0)
cv2.destroyAllWindows()