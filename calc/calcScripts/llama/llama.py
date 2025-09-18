from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class Llama:
    def __init__(self, content):
        self.model = OllamaLLM(model = "llama3.2", temperature=0.2)
        self.content = content
        self.query = """
Eres un desarrollador semi senior de RPA con experiencia en Blue Prism.
Tu tarea es analizar un documento de texto que contiene instrucciones o procesos y generar un resumen paso a paso de todas las acciones ejecutables en Blue Prism.

Reglas a seguir:

Extraer solo pasos accionables: ignora explicaciones generales, objetivos, teoría o cualquier información que no represente un paso concreto dentro del proceso.

Numerar los pasos de manera secuencial.

Asignar un nivel de complejidad a cada paso del 1 al 5:

1 = muy sencillo

5 = muy complejo
La calificación debe reflejar la perspectiva de un desarrollador semi senior.

Formato de salida:
Paso 1 [Nivel 2]: Descripción clara del paso
Paso 2 [Nivel 4]: Descripción clara del paso

Claridad y concisión: cada paso debe ser suficientemente detallado para que otro desarrollador semi senior pueda replicarlo.

Ignorar lo irrelevante: no incluir comentarios, notas o información adicional que no sean pasos concretos.

Input: {self.content}
Output esperado: lista de pasos numerados con su nivel de complejidad, siguiendo estrictamente el formato indicado.

Considerar para la dificultad:

Nivel 1: lógica posible de resolver dentro de Blue Prism (cálculos generales, uso de Excel, envío de correos y reportería).

Nivel 2: mapeo de interfaces Web o aplicativos Web. Trabajos con SAP con menos de 2 transacciones, envío de correos y reportería.

Nivel 3: trabajos con SAP con más de 3 transacciones.

Nivel 4: lógica avanzada, muchas reglas de negocio, mucho trabajo de SAP.

Nivel 5: creación de code stages personalizados para la resolución de problemas específicos.
"""

    def getTemplate(self, template_path):
        with open(template_path, "r") as template_value:
            template_value = template_value.read()
        return template_value

    def executePrompt(self, template_value, item_content):
        prompt = ChatPromptTemplate.from_template(template_value)
        chain = prompt | self.model
        result = chain.invoke({"content": item_content, "question": self.query})
        return result
    
    def modifyQuery(self, query):
        self.query = query
        return self