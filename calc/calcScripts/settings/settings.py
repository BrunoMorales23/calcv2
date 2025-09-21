import os
from os.path import join, dirname
from dotenv import load_dotenv
import sys

dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

def init():
    #global popplerPath, inputPath, tesseractPath, logsPath, promptBase, gemini_api_key, estimation_prompt, horas_prompt, template_xlsx_output, outputPath
    this = sys.modules[__name__]

    this.tesseractPath = os.environ.get("TESSERACT_EXE")
    this.popplerPath = os.environ.get("POPPLER_PATH")
    this.inputPath = os.environ.get("INPUT_PATH")
    this.logsPath = os.environ.get("LOGS_PATH")
    this.promptBase = os.environ.get("PROMPTBASE_PATH")
    this.gemini_api_key = os.environ.get("GEMINI_API_KEY")
    this.estimation_prompt = os.environ.get("PROMPT_ESTIMATION")
    this.horas_prompt = os.environ.get("PROMPT_HORAS")
    this.template_xlsx_output = os.environ.get("TEMPLATE_OUTPUT")
    this.outputPath = os.environ.get("OUTPUT_PATH")

init()