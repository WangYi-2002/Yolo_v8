import os
import sys
import time
import subprocess
import psutil
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import winsound
import winreg
import threading
import logging
import socket
from tqdm import tqdm
import locale
locale.setlocale(locale.LC_ALL, 'chs')

# === 硬编码配置 ===
class Config:
    # 基础配置
    PROJECT_PATH = r"D:\Yolo_model\Yolo_v8"  # 项目路径
    BRANCH_NAME = "main"  # 默认分支
    CHECK_INTERVAL = 300  # 检测间隔（秒）

    # 提交模板
    COMMIT_TEMPLATES = {
        "1": "bug修复",
        "2": "功能更新",
        "3": "优化性能"
    }

    # 程序元信息
    PROGRAM_NAME = "auto_git_push.exe"  # 程序名称
    DEFAULT_ICON_COLOR = "green"  # 初始图标颜色


# === 全局状态 ===
status = "正在监控"
icon_color = Config.DEFAULT_ICON_COLOR
current_branch = Config.BRANCH_NAME  # 动态跟踪当前分支


# === 检查并终止旧实例 ===
def check_and_terminate_old_instance():
    current_pid = os.getpid()
    instances_found = 0
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['exe'] and Config.PROGRAM_NAME in proc.info['exe']:
                instances_found += 1
                if proc.info['pid'] != current_pid:
                    logging.info(f"终止旧进程 {proc.info['pid']}")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    if instances_found > 1:
        logging.warning("程序已在运行，退出当前实例")
        sys.exit(0)


# === 自启动功能 ===
def add_to_startup():
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = "AutoGitPush"
    try:
        exe_path = os.path.abspath(sys.argv[0])
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_WRITE) as registry_key:
            winreg.SetValueEx(registry_key, value, 0, winreg.REG_SZ, exe_path)
        logging.info("成功添加到开机自启动")
    except Exception as e:
        logging.error(f"添加自启动失败: {e}")
        winsound.Beep(1000, 500)


# === 日志配置 ===
logging.basicConfig(
    filename='auto_git_push.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("=== 程序启动 ===")


# === 网络检测 ===
def is_connected():
    try:
        socket.create_connection(("www.baidu.com", 80), timeout=3)
        return True
    except OSError:
        return False


# === 动态图标生成 ===
def create_image(color):
    colors = {
        "green": (0, 255, 0),
        "red": (255, 0, 0),
        "yellow": (255, 255, 0),
        "blue": (0, 0, 255)
    }
    image = Image.new('RGB', (64, 64), color=colors.get(color, (0, 255, 0)))
    draw = ImageDraw.Draw(image)
    draw.text((10, 20), "Git", fill="black")
    return image


# === 更新状态和图标 ===
def update_status(icon, new_status, color="green"):
    global status, icon_color
    status = new_status
    icon_color = color
    icon.icon = create_image(icon_color)
    icon.tooltip = f"当前状态: {status}"
    icon.menu = pystray.Menu(
        item(f"状态: {status}", lambda: None),
        item("手动提交", manual_commit),
        item("切换分支", switch_branch),
        item("退出", on_exit)
    )
    logging.info(f"状态更新: {status}")


# === 退出处理 ===
def on_exit(icon, item):
    logging.info("用户退出程序")
    icon.stop()
    sys.exit(0)


# === 分支切换功能 ===
def switch_branch(icon, item):
    global current_branch
    try:
        new_branch = input("请输入新的分支名称: ")
        if new_branch:
            current_branch = new_branch
            update_status(icon, f"已切换到分支 {current_branch}", "blue")
    except Exception as e:
        logging.error(f"切换分支失败: {e}")


# === 获取文件最后修改时间 ===
def get_last_mod_time(path):
    latest_time = 0
    for root, dirs, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                mod_time = os.path.getmtime(fpath)
                if mod_time > latest_time:
                    latest_time = mod_time
            except:
                pass
    return latest_time


# === 带进度条的Git操作 ===
def run_git_command(command, desc):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with tqdm(total=100, desc=desc, ncols=70) as pbar:
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    pbar.update(10)
                    logging.info(output.strip())
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
    except Exception as e:
        raise e


# === 自动推送功能 ===
def auto_push(icon):
    global status
    if not is_connected():
        update_status(icon, "网络不可用", "red")
        winsound.Beep(1000, 500)
        logging.warning("网络连接不可用")
        return

    os.chdir(Config.PROJECT_PATH)
    try:
        update_status(icon, "推送中...", "yellow")
        run_git_command(["git", "add", "."], "添加文件")
        commit_msg = f"Auto commit {time.strftime('%Y-%m-%d %H:%M:%S')}"
        run_git_command(["git", "commit", "-m", commit_msg], "提交更改")
        run_git_command(["git", "push", "origin", current_branch], "推送代码")
        update_status(icon, "推送成功", "green")
        logging.info("✅ 自动推送成功")
    except Exception as e:
        update_status(icon, f"推送失败: {str(e)}", "red")
        logging.error(f"推送失败: {e}")
        winsound.Beep(1000, 500)


# === 手动提交功能 ===
def manual_commit(icon, item):
    try:
        print("可用的提交模板:")
        for key, value in Config.COMMIT_TEMPLATES.items():
            print(f"{key}: {value}")
        choice = input("输入模板编号或直接输入原因: ")
        commit_reason = Config.COMMIT_TEMPLATES.get(choice, choice) if choice else "手动提交"

        update_status(icon, "提交中...", "yellow")
        run_git_command(["git", "add", "."], "添加文件")
        commit_msg = f"手动提交: {commit_reason} ({time.strftime('%Y-%m-%d %H:%M:%S')})"
        run_git_command(["git", "commit", "-m", commit_msg], "提交更改")
        run_git_command(["git", "push", "origin", current_branch], "推送代码")
        update_status(icon, "手动提交成功", "green")
        logging.info(f"手动提交成功: {commit_reason}")
    except Exception as e:
        update_status(icon, f"提交失败: {str(e)}", "red")
        logging.error(f"手动提交失败: {e}")
        winsound.Beep(1000, 500)


# === 文件改动监控 ===
def monitor_changes(icon):
    global status
    last_mod_time = get_last_mod_time(Config.PROJECT_PATH)
    while True:
        time.sleep(Config.CHECK_INTERVAL)
        current_mod_time = get_last_mod_time(Config.PROJECT_PATH)
        if current_mod_time > last_mod_time:
            update_status(icon, "检测到改动", "yellow")
            auto_push(icon)
            last_mod_time = current_mod_time


# === 启动监控线程 ===
def setup_monitoring_thread(icon):
    thread = threading.Thread(target=monitor_changes, args=(icon,))
    thread.daemon = True
    thread.start()
    logging.info("文件改动监控线程已启动")


# === 系统托盘初始化 ===
def setup_tray():
    icon = pystray.Icon(
        "GitPush",
        create_image(icon_color),
        menu=pystray.Menu(
            item(f"状态: {status}", lambda: None),
            item("手动提交", manual_commit),
            item("切换分支", switch_branch),
            item("退出", on_exit)
        )
    )
    icon.tooltip = f"当前状态: {status}"
    return icon


# === 主程序入口 ===
if __name__ == "__main__":
    check_and_terminate_old_instance()
    add_to_startup()
    icon = setup_tray()
    setup_monitoring_thread(icon)
    icon.run()