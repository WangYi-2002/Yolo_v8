import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, \
    QProgressBar, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


class FruitRecognitionUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("水果识别系统")
        self.setGeometry(100, 100, 800, 600)

        # 创建主布局
        main_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()

        # 功能按钮区域（上下分布）
        self.button_layout = QVBoxLayout()
        self.load_button = QPushButton("上传图片")
        self.predict_button = QPushButton("开始识别")
        self.button_layout.addWidget(self.load_button)
        self.button_layout.addWidget(self.predict_button)
        left_layout.addLayout(self.button_layout)

        # 图片展示区，调整为较小的尺寸
        self.image_label = QLabel("未上传图片")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 200)  # 控制图片区域大小
        left_layout.addWidget(self.image_label)

        # 右侧布局
        right_layout = QVBoxLayout()

        # 预测结果展示
        self.result_label = QLabel("预测结果: 未识别")
        self.result_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.result_label)

        # 显示预测图片
        self.result_image_label = QLabel("预测结果图片")
        self.result_image_label.setAlignment(Qt.AlignCenter)
        self.result_image_label.setFixedSize(400, 200)  # 控制图片区域大小
        right_layout.addWidget(self.result_image_label)

        # 进度条和预测结果文字显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.result_text_label = QLabel("正在预测...")

        # 设置进度条
        self.progress_layout = QVBoxLayout()
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.result_text_label)
        right_layout.addLayout(self.progress_layout)

        # 将左右布局添加到主布局中
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # 设置主窗口布局
        self.setLayout(main_layout)

        # 连接信号和槽
        self.load_button.clicked.connect(self.load_image)
        self.predict_button.clicked.connect(self.start_prediction)

    def load_image(self):
        # 选择图片文件
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "所有文件 (*)", options=options)

        if file_name:
            # 更新图片展示区
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def start_prediction(self):
        # 模拟开始识别
        self.progress_bar.setValue(0)
        self.result_text_label.setText("正在预测...")

        # 模拟预测过程
        for i in range(101):
            QTimer.singleShot(i * 50, lambda value=i: self.update_progress(value))

    def update_progress(self, value):
        # 更新进度条
        self.progress_bar.setValue(value)

        # 模拟识别完成
        if value == 100:
            self.result_text_label.setText("预测完成")
            # 更新预测结果图像（模拟）
            pixmap = QPixmap("result_image.png")  # 这里可以替换成实际的预测结果图片路径
            pixmap = pixmap.scaled(self.result_image_label.size(), Qt.KeepAspectRatio)
            self.result_image_label.setPixmap(pixmap)
            self.result_label.setText("预测结果: 水果A")  # 根据实际预测结果更新


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FruitRecognitionUI()
    window.show()
    sys.exit(app.exec_())
