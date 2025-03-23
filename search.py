import os

# 定义路径
paths = [
    r"D:\Yolo_model\Yolo_v8\fruits\train\images",
    r"D:\Yolo_model\Yolo_v8\fruits\valid\images",
    r"D:\Yolo_model\Yolo_v8\fruits\test\images"
]

# 检查每个路径
for path in paths:
    print(f"Checking {path}: {os.path.exists(path)}")
