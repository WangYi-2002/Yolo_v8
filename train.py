# 训练脚本
from ultralytics import YOLO
import multiprocessing  # 导入 multiprocessing 模块

# 基础配置
model = YOLO('yolov8n.pt')  # 预训练模型
config = {
    'data': r'D:\Yolo_model\Yolo_v8\fruits\data.yaml',  # 数据集配置文件
    'epochs': 50,             # 训练轮数
    'imgsz': 640,              # 输入尺寸
    'device': '0',             # GPU设备
}

# 启动训练
def main():
    results = model.train(**config)

if __name__ == '__main__':
    multiprocessing.freeze_support()  # 调用 freeze_support()
    main()  # 调用主函数
