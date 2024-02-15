import os
import requests
import time
import threading
import math
from alive_progress import alive_bar

# 配置参数
oslists = {"android", "ios"} # 获取平台
base_url = f"https://cdn.megagamelog.com/cross/release/_getos_/curr_1/" # 基础链接
tr = 4 # 线程数
logs = False # 记录下载


t = time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())
suc, fail = [0, 0]
threads = []
osnum = {}


# 读取文件
with open("ilist.txt", "r", encoding='utf-8-sig') as file_i:
    items = file_i.read().split('\n')
with open("dirlist.txt", "r", encoding='utf-8-sig') as file_d:
    dirs = file_d.read().split(',')


# 创建目录
print("Set dirs.")
if logs:
    os.makedirs(f"logs", exist_ok=True)
for oslist in oslists:
    for dir in dirs:
        os.makedirs(f"{oslist}/{dir}", exist_ok=True)
with alive_bar(len(dirs)) as bar:
    bar(len(dirs))
#os.system('cls')
    

# 下载线程
def dl_file(url, itemg, getos):
    global suc, fail, bar

    for item in itemg:
        response = requests.get(url+item)

        if str(response) != '<Response [404]>':
            with open(f"{getos}/{item}", 'wb') as f:
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
                time.sleep(180/len(items))
                bar()
    suc, fail = [0, 0]
    bar(0)
    print(f"Download - \"{oslist}\" Assets.")
    osnum[oslist] = dl_files(oslist)
    i += 1
    #os.system('cls')


# 返回结果
i = 1
for oslist in oslists:
    if i != 1:
        print(" | ",end="")
    print(f"\"{oslist}\": {osnum[oslist]}",end="")
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
            f.write(f"\"{oslist}\": {osnum[oslist]}")
            i += 1
        f.write(f"\n")
