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
    path = os.path.join(logPath, str(today.year), str(today.month), str(today.day), "/")
    path = path.replace("\\","/")
    #try:
    os.mkdir(path)
    print(Fore.GREEN +"------------------------------------")
    print(Fore.GREEN +"Directorio creado correctamente.")
    #except FileExistsError:
    #    pass
    #except:
    #    print(Fore.RED +"------------------------------------")
    #    print(Fore.RED +"No se pudo crear el directorio para la ejecución")
    return