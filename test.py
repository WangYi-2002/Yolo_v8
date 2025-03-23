# yolo_predict.py
# Ultralytics YOLOv8 预测脚本（支持GPU加速）
# 运行命令：python yolo_predict.py --source "输入源" --model "模型路径"

import argparse
from pathlib import Path
from ultralytics import YOLO


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='YOLOv8 目标检测预测脚本')
    parser.add_argument('--source', type=str, default='https://ultralytics.com/images/bus.jpg',
                        help='输入源（文件/文件夹/摄像头ID/URL）')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='模型路径（默认使用官方yolov8n.pt）')
    parser.add_argument('--conf', type=float, default=0.5,
                        help='置信度阈值（0-1，默认0.5）')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='推理尺寸（默认640）')
    parser.add_argument('--device', type=str, default='0',
                        help='计算设备（"0"=GPU，"cpu"=CPU，默认GPU）')
    parser.add_argument('--save', action='store_true',
                        help='保存检测结果（默认保存到runs/detect）')
    parser.add_argument('--show', action='store_true',
                        help='实时显示检测结果窗口')
    args = parser.parse_args()

    try:
        # 检查本地文件是否存在（如果是文件路径）
        if not args.source.startswith(('http', 'rtsp')) and not Path(args.source).exists():
            raise FileNotFoundError(f"输入文件 {args.source} 不存在")

        # 加载模型
        model = YOLO(args.model)

        # 执行预测
        results = model.predict(
            source=args.source,
            conf=args.conf,
            imgsz=args.imgsz,
            device=args.device,
            save=args.save,
            show=args.show,
            verbose=False  # 关闭冗余输出
        )

        # 输出结果信息
        if results:
            print(f"检测到 {len(results[0])} 个目标")
            print(f"结果保存至：{results[0].save_dir}")

    except Exception as e:
        print(f"错误发生：{str(e)}")


if __name__ == "__main__":
    main()