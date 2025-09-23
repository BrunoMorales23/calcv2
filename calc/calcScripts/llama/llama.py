from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class Llama:
    def __init__(self, content):
        self.model = OllamaLLM(model = "llama3.2", temperature=0.2)
        self.content = content
        self.query = """
Eres un desarrollador semi senior de RPA con experiencia en Blue Prism.
Tu tarea es analizar un documento de texto que contiene instrucciones o procesos y generar un resumen paso a paso de todas las acciones ejecutables en Blue Prism, asignando también un rango de horas estimadas de desarrollo.

Reglas a seguir:

1. Extraer solo pasos accionables: ignora explicaciones generales, objetivos, teoría o cualquier información que no represente un paso concreto dentro del proceso.
2. Numerar los pasos de manera secuencial.
3. Asignar un nivel de complejidad del 1 al 5:
   - Nivel 1: lógica posible de resolver dentro de Blue Prism (cálculos generales, uso de Excel, envío de correos y reportería).
   - Nivel 2: mapeo de interfaces Web o aplicativos Web. Trabajos con SAP con menos de 2 transacciones, envío de correos y reportería.
   - Nivel 3: trabajos con SAP con más de 3 transacciones.
   - Nivel 4: lógica avanzada, muchas reglas de negocio, mucho trabajo de SAP.
   - Nivel 5: creación de code stages personalizados para la resolución de problemas específicos.
4. Para cada paso asigna un rango de horas estimadas en función de su nivel de complejidad:
   - Nivel 1: 1 a 3 horas
   - Nivel 2: 4 a 8 horas
   - Nivel 3: 8 a 24 horas
   - Nivel 4: 24 a 48 horas
   - Nivel 5: 48 a 80 horas
5. Si un paso contiene múltiples sub-acciones dentro de la misma instrucción, asigna el valor superior del rango.
6. Si un paso es simple y directo, asigna el valor inferior del rango.
7. Mantén la numeración, la descripción clara del paso y su nivel de complejidad.
8. Añade al final de cada paso la estimación en horas.

Formato de salida esperado:

Paso 1 [Nivel 2]: Descripción clara del paso — Estimación: 6 horas  
Paso 2 [Nivel 4]: Descripción clara del paso — Estimación: 30 horas  

Input: {content}  
Output esperado: lista de pasos numerados con nivel de complejidad y estimación de horas, siguiendo estrictamente el formato indicado.

"""

    def getTemplate(self, template_path):
        with open(template_path, "r") as template_value:
            template_value = template_value.read()
        return template_value

    def executePrompt(self, template_value, item_content):
        prompt = ChatPromptTemplate.from_template(self.query)
        chain = prompt | self.model
        result = chain.invoke({"content": item_content})
        return result
    
    def modifyQuery(self, query):
        self.query = query
        return self