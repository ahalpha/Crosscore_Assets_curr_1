import os
import time
from alive_progress import alive_bar

dt = 1500 # 循环延迟：秒
t = 300000 # 进度条梯度

i = 1
while True:
    os.system("D:/Git/bin/bash.exe push.sh")
    print(f"Waiting check...")
    with alive_bar(t) as bar:
        bar(0)
        for a in range(t-1):
            time.sleep(dt/t)
            bar()
    i += 1