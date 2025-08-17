import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

def init():
    global popplerPath, inputPath, tesseractPath, logsPath
    tesseractPath = os.environ.get("TESSERACT_EXE")
    popplerPath = os.environ.get("POPPLER_PATH")
    inputPath = os.environ.get("INPUT_PATH")
    logsPath = os.environ.get("LOGS_PATH")