from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # 确保文件路径正确
model.train(data="D:/Yolo_model/Yolo_v8/fruits/data.yaml", epochs=3)
model.val()
model.export(format="onnx")
