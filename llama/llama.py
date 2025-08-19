from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class Llama:
    def __init__(self):
        self.model = OllamaLLM(model = "llama3.2", temperature=0.2)
        self.query = "¿Cuántas aplicaciones se usan?, ¿Es necesario hacer reporte de ejecución?"

    def getTemplate(self, template_path):
        with open(template_path, "r") as template_value:
            template_value = template_value.read()
        return template_value

    def executePrompt(self, template_value, item_content):
        prompt = ChatPromptTemplate.from_template(template_value)
        chain = prompt | self.model
        result = chain.invoke({"content": item_content, "question": self.query})
        print(result)
        return result