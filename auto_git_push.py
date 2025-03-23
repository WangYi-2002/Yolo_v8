import os
os.system("chcp 65001")  # 设置命令行为 UTF-8 编码
import sys
import time
import subprocess
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import winsound
import winreg  # 用于修改 Windows 注册表，添加自启动
import threading  # 使用线程避免阻塞UI

# === 配置部分 ===
project_path = r"D:\Yolo_model\Yolo_v8"  # 你的项目路径
branch_name = "main"  # Git 分支名
check_interval = 60  # 检测改动时间间隔，单位秒
status = "正在监控"  # 初始状态

# === 创建托盘图标 ===
def create_image():
    image = Image.new('RGB', (64, 64), color=(0, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((10, 20), "Git", fill="black")
    return image

# === 托盘退出 ===
def on_exit(icon, item):
    print("退出程序")
    icon.stop()

# === 更新托盘状态 ===
def update_status(icon, new_status):
    global status
    status = new_status
    icon.icon = create_image()  # 更新托盘图标
    icon.tooltip = f"当前状态: {status}"  # 鼠标悬停显示当前状态
    icon.menu = pystray.Menu(item(f"状态: {status}", on_exit), item("手动提交", manual_commit))

# === 自动提交和推送 ===
def auto_push(icon):
    global status
    os.chdir(project_path)
    try:
        update_status(icon, "检测到改动，正在推送...")
        subprocess.run(["git", "add", "."], check=True)
        commit_msg = f"Auto commit {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", branch_name], check=True)
        update_status(icon, "推送成功")
        print(f"[{time.strftime('%H:%M:%S')}] ✅ 自动推送成功")
    except subprocess.CalledProcessError as e:
        update_status(icon, "推送失败")
        print(f"[{time.strftime('%H:%M:%S')}] ⚠️ 推送失败: {e}")
        winsound.Beep(1000, 500)  # 发出错误提示音

# === 获取最近修改时间 ===
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

# === 自动检测文件改动并提交 ===
def monitor_changes(icon):
    global status
    last_mod_time = get_last_mod_time(project_path)
    while True:
        time.sleep(check_interval)
        current_mod_time = get_last_mod_time(project_path)
        if current_mod_time != last_mod_time:
            update_status(icon, "正在推送...")
            print(f"[{time.strftime('%H:%M:%S')}] 📝 检测到改动，正在推送...")
            auto_push(icon)
            last_mod_time = current_mod_time

# === 手动提交功能 ===
def manual_commit(icon, item):
    try:
        # 获取提交原因
        commit_reason = input("请输入手动提交的原因: ")  # 在命令行获取输入

        # 如果用户没有输入原因，使用默认提交信息
        if not commit_reason:
            commit_reason = "手动提交，无明确原因"

        update_status(icon, "手动提交中...")
        print(f"手动提交中... {time.strftime('%H:%M:%S')}")
        os.chdir(project_path)
        subprocess.run(["git", "add", "."], check=True)

        # 创建带有原因的提交消息
        commit_msg = f"手动提交: {commit_reason} ({time.strftime('%Y-%m-%d %H:%M:%S')})"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", branch_name], check=True)

        update_status(icon, "手动提交成功")
        print(f"[{time.strftime('%H:%M:%S')}] 手动提交成功: {commit_reason}")
    except subprocess.CalledProcessError as e:
        update_status(icon, "手动提交失败")
        print(f"[{time.strftime('%H:%M:%S')}] 手动提交失败: {e}")
        winsound.Beep(1000, 500)  # 发出错误提示音


# === 托盘图标和菜单设置 ===
def setup_tray():
    icon = pystray.Icon("GitPush", create_image(), menu=pystray.Menu(item(f"状态: {status}", on_exit), item("手动提交", manual_commit)))
    icon.tooltip = f"当前状态: {status}"  # 鼠标悬停显示当前状态
    icon.run()  # 启动托盘图标并保持运行

# === 启动监控线程 ===
def setup_monitoring_thread(icon):
    thread = threading.Thread(target=monitor_changes, args=(icon,))
    thread.daemon = True
    thread.start()

# === 自启动功能 ===
def add_to_startup():
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = "AutoGitPush"
    exe_path = os.path.join(os.getcwd(), "auto_git_push.exe")  # 确保 exe 文件路径正确
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_WRITE) as registry_key:
            winreg.SetValueEx(registry_key, value, 0, winreg.REG_SZ, exe_path)
        print("程序已成功添加到开机自启动。")
    except Exception as e:
        print(f"添加自启动失败: {e}")

# === 启动程序 ===
if __name__ == "__main__":
    add_to_startup()  # 程序自启动
    setup_tray()  # 初始化托盘图标
