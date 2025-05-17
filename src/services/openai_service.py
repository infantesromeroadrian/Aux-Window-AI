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
        self.models = ["gpt-4", "gpt-3.5-turbo"]
        
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
Tu objetivo es proporcionar sugerencias útiles y concisas durante la conversación.
Ofrece:
1. Respuestas convincentes a las preguntas del cliente
2. Puntos clave para mencionar según el contexto de la conversación
3. Soluciones para resolver objeciones comunes
4. Oportunidades de venta cruzada cuando sea apropiado

Las sugerencias deben ser breves (1-3 frases), directas y fácilmente aplicables.
Responde SIEMPRE en español.
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
                        {"role": "user", "content": conversation_text}
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
Debes proporcionar respuestas detalladas, informativas y útiles a las preguntas sobre:
- Técnicas de venta y negociación
- Manejo de objeciones de clientes
- Información sobre productos y servicios típicos
- Estrategias para cerrar ventas
- Servicio al cliente y fidelización

Tus respuestas deben ser profesionales, precisas y orientadas a ayudar al agente comercial a tener éxito.
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
                        {"role": "user", "content": question}
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