import os

def getdircontent():
    i_list = []

    files = os.listdir("./inputs/")
    for i in range(len(files)):
        file = files[i]
        if file.count(".docx") == 0:
            print(f"Este doc debe ser eliminado: {file}")
            i_list.append(i)

    i_list.sort(reverse=True)
    for i in i_list:
        files.pop(i)

    print(files)
    return files

getdircontent()