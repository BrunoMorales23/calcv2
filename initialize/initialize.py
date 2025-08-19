import os
from colorama import Fore, init
import datetime

init(autoreset=True)

def getDirContent(dir):
    i_list = []

    files = os.listdir(dir)
    for i in range(len(files)):
        file = files[i]
        if file.count(".pdf") == 0:
            i_list.append(i)

    i_list.sort(reverse=True)
    for i in i_list:
        files.pop(i)

    print(files)
    return files

def createDir(logPath):
    today = datetime.datetime.now()
    logPath = os.path.join("logs", str(today.year), str(today.month), str(today.day))
    os.makedirs(logPath, exist_ok=True)
    return logPath