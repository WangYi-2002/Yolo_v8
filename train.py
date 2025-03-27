import os
import subprocess

from ultralytics import YOLO
import torch

# 1. 环境检查
print("=" * 50)
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"CUDA版本: {torch.version.cuda}")
print(f"当前设备: {torch.cuda.get_device_name(0)}")
print("=" * 50)


# 2. 训练配置
def train_yolov8():
    # 数据集路径（Windows需使用原始字符串或双反斜杠）
    data_path = r"D:\Yolo_model\Yolo_v8\fruits\data.yaml"

    # 检查数据集是否存在
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"数据集配置文件不存在: {data_path}")

    # 加载模型
    model = YOLO("yolov8n.pt")  # 从预训练权重初始化

    # 训练参数（与你YAML完全一致）
    train_args = {
        "data": data_path,
        "epochs": 100,
        "batch": 8,  # RTX 3060可尝试减小到8-12防OOM
        "imgsz": 640,
        "device": "0",  # 使用GPU 0
        "workers": 4,  # Windows建议设为4或更小
        "name": "train4",  # 实验名称
        "patience": 50,  # 早停轮次
        "pretrained": True,  # 使用预训练权重
        "optimizer": "auto",  # 自动选择优化器
        "verbose": True,  # 打印详细日志
        "val": True,  # 启用验证
        "plots": True,  # 生成训练曲线图
        "augment": False,  # 关闭数据增强（你配置中为False）
        "lr0": 0.01,  # 初始学习率
        "lrf": 0.01,  # 最终学习率
        "momentum": 0.937,
        "weight_decay": 0.0005,
        "box": 7.5,  # 定位损失权重
        "cls": 0.5,  # 分类损失权重
        "hsv_h": 0.015,  # 色相增强
        "hsv_s": 0.7,  # 饱和度增强
        "hsv_v": 0.4,  # 明度增强
        "fliplr": 0.5,  # 水平翻转概率
    }

    # 开始训练
    results = model.train(**train_args)

    # 训练完成后验证
    metrics = model.val()
    print(f"\n验证结果 mAP50-95: {metrics.box.map:.4f}")

    # 自动启动TensorBoard
    log_dir = os.path.join("runs", "detect", "train4")
    subprocess.Popen(f"tensorboard --logdir={log_dir} --port=6006", shell=True)
    print(f"TensorBoard已启动: http://localhost:6006")

if __name__ == "__main__":
    train_yolov8()