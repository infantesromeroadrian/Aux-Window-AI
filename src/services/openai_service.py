import os
import openai
from typing import Dict, Any

class OpenAIService:
    """Service to handle interactions with OpenAI API."""
    
    def __init__(self):
        """Initialize the OpenAI service with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key not found in environment variables")
        
        # Set API key directly - this works with openai 0.28.1
        openai.api_key = self.api_key
        
        # Lista de modelos a intentar, en orden de preferencia (para versión 0.28.1)
        self.models = ["gpt-4", "gpt-4.1"]
        
    def get_suggestions(self, conversation_text: str) -> Dict[str, Any]:
        """
        Get suggestions based on conversation text.
        
        Args:
            conversation_text: The transcription text from the conversation
            
        Returns:
            Dictionary with suggestions and metadata
        """
        if not conversation_text or conversation_text.strip() == "":
            return {
                "success": False,
                "error": "No se proporcionó texto para generar sugerencias"
            }
            
        # Sistema de contenido para el asistente
        system_content = """
Eres un asistente para agentes comerciales que están en llamadas con clientes.
IMPORTANTE: Estás recibiendo una transcripción en TIEMPO REAL de una conversación en curso. 
El texto se está generando progresivamente mediante dictado de voz, por lo que recibirás fragmentos
incrementales de la conversación. Cada vez, analiza SOLO lo que tienes disponible hasta ese momento.

Tu objetivo es proporcionar sugerencias útiles y concisas que sean relevantes para el estado ACTUAL 
de la conversación, incluso si está incompleta o en desarrollo.

Ofrece:
1. Respuestas convincentes a las preguntas del cliente que has identificado hasta ahora
2. Puntos clave para mencionar según el contexto disponible
3. Soluciones para resolver objeciones que hayas detectado
4. Oportunidades de venta cruzada cuando sea apropiado

Las sugerencias deben ser:
- Breves (1-3 frases)
- Directas y fácilmente aplicables en el momento actual de la conversación
- Adaptadas al fragmento de conversación disponible, sin asumir información que no se ha proporcionado

Responde SIEMPRE en español y ten en cuenta que la conversación sigue en desarrollo.
"""
            
        # Intentar diferentes modelos en orden (sintaxis para versión 0.28.1)
        last_error = None
        for model in self.models:
            try:
                # Usar la sintaxis compatible con openai==0.28.1
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": f"Transcripción en curso de una llamada comercial (texto parcial hasta ahora):\n\n{conversation_text}"}
                    ],
                    temperature=0.7,
                    max_tokens=150
                )
                
                return {
                    "success": True, 
                    "suggestions": response.choices[0].message['content'],
                    "model": response.model
                }
                
            except Exception as e:
                last_error = str(e)
                print(f"Error con el modelo {model}: {last_error}")
                # Continuar con el siguiente modelo
                continue
                
        # Si llegamos aquí, todos los modelos han fallado
        return {
            "success": False,
            "error": f"No se pudo generar sugerencias. Último error: {last_error}"
        }
        
    def get_answer_to_question(self, question: str) -> Dict[str, Any]:
        """
        Get answer to a direct question.
        
        Args:
            question: The question to answer
            
        Returns:
            Dictionary with answer and metadata
        """
        if not question or question.strip() == "":
            return {
                "success": False,
                "error": "No se proporcionó ninguna pregunta"
            }
            
        # Sistema de contenido para el asistente
        system_content = """
Eres un asistente de ventas experto, especializado en responder consultas de agentes comerciales.
Debes entender que el agente está en una llamada en vivo con un cliente en este momento, 
por lo que necesita respuestas rápidas y accionables inmediatamente.

Debes proporcionar respuestas detalladas, informativas y útiles a las preguntas sobre:
- Técnicas de venta y negociación
- Manejo de objeciones de clientes
- Información sobre productos y servicios típicos
- Estrategias para cerrar ventas
- Servicio al cliente y fidelización

Tus respuestas deben ser profesionales, precisas y orientadas a ayudar al agente comercial a tener éxito
en la conversación que está teniendo AHORA MISMO. Prioriza la inmediatez y aplicabilidad.

Incluye ejemplos prácticos cuando sea relevante y proporciona consejos accionables.
Responde SIEMPRE en español y de forma completa y profesional.
"""
            
        # Intentar diferentes modelos en orden
        last_error = None
        for model in self.models:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": f"Pregunta urgente durante una llamada con cliente: {question}"}
                    ],
                    temperature=0.7,
                    max_tokens=500  # Permitimos respuestas más largas para preguntas directas
                )
                
                return {
                    "success": True, 
                    "answer": response.choices[0].message['content'],
                    "model": response.model
                }
                
            except Exception as e:
                last_error = str(e)
                print(f"Error con el modelo {model} al responder pregunta: {last_error}")
                # Continuar con el siguiente modelo
                continue
                
        # Si llegamos aquí, todos los modelos han fallado
        return {
            "success": False,
            "error": f"No se pudo responder la pregunta. Último error: {last_error}"
        }
        
    def analyze_sentiment(self, conversation_text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of the customer based on the conversation text.
        
        Args:
            conversation_text: The conversation text to analyze
            
        Returns:
            Dictionary with sentiment analysis results
        """
        if not conversation_text or conversation_text.strip() == "":
            return {
                "success": False,
                "error": "No hay texto de conversación para analizar"
            }
            
        # Sistema de contenido para análisis de sentimiento
        system_content = """
Eres un analista experto en emociones y sentimientos humanos durante conversaciones.

IMPORTANTE: Estás analizando una transcripción en TIEMPO REAL que se está generando progresivamente
por dictado de voz. Esta conversación está en curso y puede estar incompleta. Tu análisis debe
adaptarse al fragmento disponible hasta ahora.

Analiza el texto proporcionado (que es una transcripción parcial de una conversación con un cliente) 
y determina:

1. Sentimiento general del cliente hasta este momento (muy negativo, negativo, neutral, positivo, muy positivo)
2. Emociones predominantes detectadas hasta ahora (frustración, confusión, interés, satisfacción, etc.)
3. Nivel de interés del cliente según lo observado (bajo, medio, alto)
4. Posibles preocupaciones o dudas identificadas en el fragmento actual
5. Recomendaciones específicas sobre cómo el agente debería ajustar su enfoque en los próximos momentos

Proporciona tu análisis en un formato estructurado, breve y directo.
Tu respuesta debe ser útil para un agente comercial que necesita entender el estado emocional
del cliente rápidamente para ajustar su estrategia en tiempo real.

Considera que la conversación sigue en desarrollo y que tu análisis se basa en información parcial.
Responde SIEMPRE en español.
"""
            
        # Intentar diferentes modelos en orden
        last_error = None
        for model in self.models:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": f"Fragmento de transcripción en tiempo real de una llamada comercial:\n\n{conversation_text}"}
                    ],
                    temperature=0.5,
                    max_tokens=300
                )
                
                return {
                    "success": True, 
                    "sentiment_analysis": response.choices[0].message['content'],
                    "model": response.model
                }
                
            except Exception as e:
                last_error = str(e)
                print(f"Error con el modelo {model} al analizar sentimiento: {last_error}")
                # Continuar con el siguiente modelo
                continue
                
        # Si llegamos aquí, todos los modelos han fallado
        return {
            "success": False,
            "error": f"No se pudo analizar el sentimiento. Último error: {last_error}"
        }
        
    def generate_call_summary(self, conversation_text: str) -> Dict[str, Any]:
        """
        Generate a summary of the call with key points and follow-up tasks.
        
        Args:
            conversation_text: The complete conversation text
            
        Returns:
            Dictionary with call summary
        """
        if not conversation_text or conversation_text.strip() == "":
            return {
                "success": False,
                "error": "No hay texto de conversación para resumir"
            }
            
        # Sistema de contenido para resumen de llamada
        system_content = """
Eres un asistente especializado en analizar y resumir conversaciones de ventas.

IMPORTANTE: La transcripción que recibes proviene de un dictado en tiempo real y puede estar
incompleta o contener fragmentos parciales. Debes adaptar tu resumen al contenido disponible
hasta este momento, reconociendo que la conversación puede estar en curso.

Basándote en la transcripción de la llamada disponible hasta ahora, genera un resumen estructurado que incluya:

1. RESUMEN GENERAL: Una descripción breve (2-3 frases) de la conversación según lo que se ha capturado.
2. PUNTOS CLAVE: Lista de 3-5 puntos importantes identificados en el fragmento disponible.
3. INTERESES DEL CLIENTE: Productos o servicios específicos que parecen interesar al cliente según lo transcrito.
4. OBJECIONES: Cualquier duda o preocupación expresada por el cliente hasta el momento.
5. ACCIONES DE SEGUIMIENTO: Lista de tareas concretas que el agente debería realizar como seguimiento.
6. OPORTUNIDADES: Posibles oportunidades de venta adicionales identificadas en el texto disponible.

Si alguna sección no tiene suficiente información para ser completada, indícalo explícitamente.

Tu resumen debe ser claro, conciso y directamente aplicable para el agente comercial,
teniendo en cuenta el carácter parcial o en desarrollo de la conversación.
Debe proporcionar valor práctico para el seguimiento posterior a la llamada.

Responde SIEMPRE en español y en formato estructurado.
"""
            
        # Intentar diferentes modelos en orden
        last_error = None
        for model in self.models:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": f"Transcripción de llamada comercial (posiblemente en curso o incompleta):\n\n{conversation_text}"}
                    ],
                    temperature=0.5,
                    max_tokens=800  # Permitimos respuestas más largas para resúmenes
                )
                
                return {
                    "success": True, 
                    "call_summary": response.choices[0].message['content'],
                    "model": response.model
                }
                
            except Exception as e:
                last_error = str(e)
                print(f"Error con el modelo {model} al generar resumen: {last_error}")
                # Continuar con el siguiente modelo
                continue
                
        # Si llegamos aquí, todos los modelos han fallado
        return {
            "success": False,
            "error": f"No se pudo generar el resumen de la llamada. Último error: {last_error}"
        } 