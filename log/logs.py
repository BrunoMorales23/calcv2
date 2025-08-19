import datetime

def createNewLog(log_path):
    localtime = datetime.datetime.now()
    localtime = str(localtime.day) + " " + str(localtime.month)
    namefile = "Log "+ str(localtime)
    log_path = str(log_path) + "\\" + str(namefile) + ".txt"
    try:
        open(log_path, "x")
    except FileExistsError:
        print("Log ya creado")
    except:
        raise Exception("Falló al crear Log para la ejecución")
    print(log_path)
    return log_path


def writeLogValue(current_log, writting_value):
    with open(str(current_log), "w") as f:
        f.write(f"{datetime.datetime.now()}:  {writting_value}")

if __name__ == "__main__":
    createNewLog()