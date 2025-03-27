from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainterPath, QRegion


class FruitRecognitionUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("水果识别系统")  # 设置窗口标题
        self.setGeometry(100, 100, 900, 600)  # 设置窗口初始位置和大小
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏自带的导航栏，创建无边框窗口

        # 变量用于窗口拖动
        self.old_pos = None

        # 设置窗口的圆角
        self.set_round_corners()

        # 自定义导航栏
        self.navbar = QWidget(self)
        self.navbar.setGeometry(0, 0, 900, 40)
        self.navbar.setStyleSheet("background-color: #2C3E50; color: white;")
        self.navbar.mousePressEvent = self.start_move  # 绑定鼠标按下事件
        self.navbar.mouseMoveEvent = self.moving  # 绑定鼠标移动事件
        self.navbar.mouseReleaseEvent = self.end_move  # 绑定鼠标释放事件

        # 关闭按钮
        self.close_btn = QPushButton("✖", self.navbar)
        self.close_btn.setGeometry(860, 5, 30, 30)
        self.close_btn.setStyleSheet(
            "background: none; color: white; font-size: 16px; border-radius: 15px; padding: 5px;")
        self.close_btn.setCursor(Qt.PointingHandCursor)  # 设置鼠标悬停样式
        self.close_btn.clicked.connect(self.close)  # 绑定关闭窗口事件
        self.close_btn.enterEvent = self.on_hover  # 绑定鼠标进入事件
        self.close_btn.leaveEvent = self.on_leave  # 绑定鼠标离开事件

        # 左侧功能区
        self.left_widget = QWidget(self)
        self.left_widget.setGeometry(0, 40, 200, 560)
        self.left_widget.setStyleSheet("background-color: #34495E;")

        # 上传图片按钮
        self.upload_btn = QPushButton("上传图片", self.left_widget)
        self.upload_btn.setGeometry(30, 50, 140, 40)

        # 开始检测按钮
        self.detect_btn = QPushButton("开始检测", self.left_widget)
        self.detect_btn.setGeometry(30, 100, 140, 40)

        # 右侧识别结果显示区域
        self.result_label = QLabel("识别结果显示区", self)
        self.result_label.setGeometry(600, 100, 280, 400)
        self.result_label.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        # 图片展示区
        self.image_label = QLabel(self)
        self.image_label.setGeometry(220, 100, 360, 400)
        self.image_label.setStyleSheet("border: 1px solid #ccc;")

    def set_round_corners(self):
        """设置窗口的圆角效果"""
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        """当窗口大小调整时，保持圆角"""
        self.set_round_corners()
        super().resizeEvent(event)

    def set_image(self, image_path):
        """设置图片展示区的图片"""
        pixmap = QPixmap(image_path).scaled(360, 400, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def start_move(self, event):
        """记录鼠标按下位置，以便拖动窗口"""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def moving(self, event):
        """拖动窗口"""
        if self.old_pos is not None and event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def end_move(self, event):
        """鼠标释放后停止拖动"""
        self.old_pos = None

    def on_hover(self, event):
        """当鼠标悬停在关闭按钮上时，改变按钮样式"""
        self.close_btn.setStyleSheet(
            "background: red; color: white; font-size: 16px; border-radius: 15px; padding: 5px;")

    def on_leave(self, event):
        """当鼠标离开关闭按钮时，恢复原样式"""
        self.close_btn.setStyleSheet(
            "background: none; color: white; font-size: 16px; border-radius: 15px; padding: 5px;")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = FruitRecognitionUI()
    window.show()
    sys.exit(app.exec_())
