import os
import requests
import time
import threading
import math
from alive_progress import alive_bar

# 配置参数
oslists = {"android": "curr_1", "ios": "curr_new_1"} # 获取平台
tr = 4 # 线程数
dt = 180 # 多平台下载延迟：秒
logs = False # 记录详细文件下载


t = time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())
suc, fail = [0, 0]
base_url = ""
threads = []
osnum = {}


# 读取文件
with open("lists/ilist.txt", "r", encoding='utf-8-sig') as file_i:
    items = file_i.read().split('\n')
with open("lists/dirlist.txt", "r", encoding='utf-8-sig') as file_d:
    dirs = file_d.read().split(',')


# 创建目录
print("Set dirs.")
if logs:
    os.makedirs(f"logs", exist_ok=True)
for oslist in oslists:
    for dir in dirs:
        os.makedirs(f"files/{oslists[oslist]}/{oslist}/{dir}", exist_ok=True)
with alive_bar(len(dirs)) as bar:
    bar(len(dirs))
#os.system('cls')
    

# 下载线程
def dl_file(url, itemg, getos):
    global suc, fail, bar

    for item in itemg:
        response = requests.get(url+item)

        if str(response) != '<Response [404]>':
            with open(f"files/{oslists[getos]}/{getos}/{item}", 'wb') as f:
                f.write(response.content)

            if logs:
                with open(f"logs/{getos}_{t}.log", 'a+') as f:
                    f.write(f"{item} - Saved.\n")
            suc += 1
            bar()
        else:
            if logs:
                with open(f"logs/{getos}_{t}.log", 'a+') as f:
                    f.write(f"{item} - File not found.\n")
            fail += 1
            bar()

        #time.sleep(1)

# 下载文件
def dl_files(getos): 
    global suc, fail, bar

    url = base_url.replace("_getos_", getos)

    n = math.ceil(len(items)/tr)
    for itemg in [items[i:i + n] for i in range(0, len(items), n)]:
        dl = threading.Thread(target=dl_file, args=(url, itemg, getos))
        threads.append(dl)
        dl.start()

    with alive_bar(len(items)) as bar:
        for dl in threads:
            dl.join()

    return f"{suc}/{suc+fail}"

# 开始下载
i = 1
for oslist in oslists:
    if i != 1:
        print(f"Waiting check...")
        with alive_bar(len(items)) as bar:
            bar(0)
            for a in range(len(items)-1):
                time.sleep(dt/len(items))
                bar()
    suc, fail = [0, 0]
    bar(0)
    print(f"Download - \"{oslist}\" Assets.")
    base_url = f"https://cdn.megagamelog.com/cross/release/_getos_/{oslists[oslist]}/"
    osnum[f"{oslists[oslist]}-{oslist}"] = dl_files(oslist)
    i += 1
    #os.system('cls')


# 返回结果
i = 1
for oslist in oslists:
    if i != 1:
        print(" | ",end="")
    print(f"\"{oslists[oslist]}-{oslist}\": {osnum[f'{oslists[oslist]}-{oslist}']}",end="")
    i += 1
print(f"")


# 返回日志
logs_all = True
if logs_all:
    with open(f"down.log", 'a+') as f:
        f.write(f"{t} - Done. ")
        i = 1
        for oslist in oslists:
            if i != 1:
                f.write(f" | ")
            f.write(f"\"{oslists[oslist]}-{oslist}\": {osnum[f'{oslists[oslist]}-{oslist}']}")
            i += 1
        f.write(f"\n")
