# 训练脚本（无任何中文字符）
from ultralytics import YOLO

# 基础配置
model = YOLO('yolov8n.pt')  # 预训练模型
config = {
    'data': r'D:\Yolo_model\Yolo_v8\fruits\data.yaml',  # 数据集配置文件
    'epochs': 10,             # 训练轮数
    'imgsz': 640,              # 输入尺寸
    'device': '0',             # GPU设备
}

# 启动训练
results = model.train(**config)

if __name__ == '__main__':
    main()