# -*- coding: utf-8 -*-
import torch
from ultralytics import YOLO


def train_with_limited_resources():
    # 硬件优化
    torch.backends.cudnn.benchmark = True

    # 加载模型 (自动下载yolov8s.pt)
    model = YOLO("yolov8s.pt")  # 使用官方推荐的模型加载方式

    # 训练参数 (已验证可运行参数)
    train_args = {
        "data": r"D:\Yolo_model\Yolo_v8\fruits\data.yaml",
        "epochs": 5,
        "batch": 6,
        "imgsz": 640,
        "device": "0",
        "workers": 4,
        "lr0": 1e-3,
        "weight_decay": 0.01,
        "augment": False,  # 数据增强总开关
        "rect": True,  # 矩形训练节省显存
        "cos_lr": True,  # 余弦学习率调度
        "dropout": 0.1,  # 防止过拟合
        "name": "exp1",
        "patience": 30,
        "verbose": True
    }

    # 开始训练
    model.train(**train_args)

    # 验证
    model.val()


if __name__ == "__main__":
    train_with_limited_resources()