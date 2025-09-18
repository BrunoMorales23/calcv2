import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

def init():
    global popplerPath, inputPath, tesseractPath, logsPath, promptBase, gemini_api_key, estimation_prompt, horas_prompt
    tesseractPath = os.environ.get("TESSERACT_EXE")
    popplerPath = os.environ.get("POPPLER_PATH")
    inputPath = os.environ.get("INPUT_PATH")
    logsPath = os.environ.get("LOGS_PATH")
    promptBase = os.environ.get("PROMPTBASE_PATH")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    estimation_prompt = os.environ.get("PROMPT_ESTIMATION")
    horas_prompt = os.environ.get("PROMPT_HORAS")