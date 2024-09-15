import os
from PIL import Image
from planedetector import plane_detector
from ultralytics import YOLO

def ImageProcessing(tilecreator):
    """
    Processes the tiles individually before stitching them
    back together in one large image.
    
    Parameter tilecreator: the object for the matrix of
    tiles.
    """
    path = os.getcwd()
    model = YOLO(path + '/backend/src/runs/detect/train/weights/best.pt')

    # Calculates the size of the stitched image
    tile_width, tile_height = tilecreator.tiles[0][0].shape[1], tilecreator.tiles[0][0].shape[0]
    num_cols = len(tilecreator.tiles)
    num_rows = len(tilecreator.tiles[0])
    stitched_width = num_rows * tile_width
    stitched_height = num_cols * tile_height
    stitched_image = Image.new('RGB', (stitched_width, stitched_height))

    print(f"Tile Width: {tile_width}, Tile Height: {tile_height}")
    print(f"Number of Rows: {num_rows}, Number of Columns: {num_cols}")
    print(f"Stitched Image Width: {stitched_width}, Stitched Image Height: {stitched_height}")

    # Processes each individual tile and stitches them together into the larger
    # image
    num_of_planes = 0
    for i, tiles in enumerate(tilecreator.tiles):
        for j, tile in enumerate(tiles):
            print(f"Processing and stitching tile {j}, {i} of {num_rows} , {num_cols}")          
            rendered_np, planes_temp = plane_detector(model, tile, confidence_threshold = 0.7)
            num_of_planes = num_of_planes + planes_temp
            x = j * tile_height
            y = i * tile_width
            rendered_image = Image.fromarray(rendered_np)
            stitched_image.paste(rendered_image, (x, y))

    return stitched_image, num_of_planes

