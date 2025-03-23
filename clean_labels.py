import os

def clean_labels(label_dir, task_type='detect'):
    """
    task_type: 'detect' 保留检测框（class x_center y_center width height）
               'segment' 保留分割点（class x1 y1 x2 y2 ...）
    """
    for root, _, files in os.walk(label_dir):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    lines = f.readlines()
                new_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) < 2:
                        continue
                    if task_type == 'detect' and len(parts) == 5:  # 检测框
                        new_lines.append(line)
                    elif task_type == 'segment' and len(parts) > 5: # 分割点
                        new_lines.append(line)
                with open(path, 'w') as f:
                    f.writelines(new_lines)

# 执行清理（根据你的任务类型选择 'detect' 或 'segment'）
clean_labels(r"D:\Yolo_model\Yolo_v8\fruits.yolov8\train\labels", task_type='detect')
clean_labels(r"D:\Yolo_model\Yolo_v8\fruits.yolov8\valid\labels", task_type='detect')