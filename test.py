from ultralytics import YOLO
# -*- coding: utf-8 -*-
# Load a pretrained YOLO11n model
#model = YOLO("yolo11n.pt")
model = YOLO("yolov8n.pt")  # 注意正确的名称是 yolov8n.pt
# Define path to the image file
source = "ultralytics/assets/bus.jpg"

# Run inference on the source
results = model(source)  # list of Results objects