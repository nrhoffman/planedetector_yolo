from PIL import Image
from planedetector import plane_detector
from ultralytics import YOLO

def ImageProcessing(tilecreator):
    model = YOLO('runs/detect/train/weights/best.pt')
    tile_width, tile_height = tilecreator.tiles[0][0].shape[1], tilecreator.tiles[0][0].shape[0]
    num_cols = len(tilecreator.tiles)
    num_rows = len(tilecreator.tiles[0])
    stitched_width = num_rows * tile_width
    stitched_height = num_cols * tile_height
    stitched_image = Image.new('RGB', (stitched_width, stitched_height))
    stitched_image_ratio = stitched_width/stitched_height

    print(f"Tile Width: {tile_width}, Tile Height: {tile_height}")
    print(f"Number of Rows: {num_rows}, Number of Columns: {num_cols}")
    print(f"Stitched Image Width: {stitched_width}, Stitched Image Height: {stitched_height}")

    for i, tiles in enumerate(tilecreator.tiles):
        for j, tile in enumerate(tiles):
            print(f"Processing and stitching tile {j}, {i} of {num_rows} , {num_cols}")          
            rendered_np = plane_detector(model, tile, confidence_threshold = 0.65)
            x = j * tile_height
            y = i * tile_width
            rendered_image = Image.fromarray(rendered_np)
            stitched_image.paste(rendered_image, (x, y))

    return stitched_image_ratio, stitched_image

