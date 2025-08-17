import os
from colorama import init

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
