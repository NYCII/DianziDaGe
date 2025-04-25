from pynput import keyboard
from pynput.keyboard import Key, Controller
import random
import time
import win32gui
import win32process
import tkinter as tk
from tkinter import ttk
import threading

class DianZiDaGe:
    def __init__(self):
        self.keyboard_controller = Controller()
        self.last_time = time.time()
        self.interval = 0.5
        self.running = False
        self.listener = None
        self.probability = 0.3
        self.create_ui()

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title("电子打嗝")
        self.root.geometry("300x200")
        
        # 创建控制框架
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.BOTH, expand=True)

        # 开关按钮
        self.toggle_button = ttk.Button(
            control_frame, 
            text="开启打嗝", 
            command=self.toggle_service
        )
        self.toggle_button.pack(pady=10)

        # 概率滑动条
        ttk.Label(control_frame, text="打嗝概率:").pack()
        self.prob_scale = ttk.Scale(
            control_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.update_probability
        )
        self.prob_scale.set(30)
        self.prob_scale.pack(fill=tk.X, pady=10)

        # 状态标签
        self.status_label = ttk.Label(
            control_frame, 
            text="当前状态: 已停止",
            foreground="red"
        )
        self.status_label.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_probability(self, value):
        self.probability = float(value) / 100

    def toggle_service(self):
        if not self.running:
            self.running = True
            self.toggle_button.config(text="停止打嗝")
            self.status_label.config(text="当前状态: 运行中", foreground="green")
            threading.Thread(target=self.start, daemon=True).start()
        else:
            self.running = False
            self.toggle_button.config(text="开启打嗝")
            self.status_label.config(text="当前状态: 已停止", foreground="red")
            if self.listener:
                self.listener.stop()

    def on_press(self, key):
        try:
            if not self.running:
                return
            current_time = time.time()
            if current_time - self.last_time >= self.interval:
                if hasattr(key, 'char') and random.random() < self.probability:
                    self.keyboard_controller.type(key.char)
                self.last_time = current_time
        except AttributeError:
            pass

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.listener = listener
            listener.join()

    def on_closing(self):
        self.running = False
        if self.listener:
            self.listener.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    dage = DianZiDaGe()
    dage.run()