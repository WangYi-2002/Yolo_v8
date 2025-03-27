from ultralytics import YOLO

# 加载训练好的模型
model = YOLO("runs/detect/train/weights/best.pt")

# 预测示例
results = model.predict("C:/Users/wy199/Desktop/Snipaste_2025-03-27_11-28-43.png", save=True)