from ultralytics import YOLO

model = YOLO('../model.yaml', task='detect')

model.train(data='../data.yaml')