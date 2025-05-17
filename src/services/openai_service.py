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
        
    def get_suggestions(self, conversation_text: str, language: str = 'es-ES') -> Dict[str, Any]:
        """
        Get suggestions based on conversation text.
        
        Args:
            conversation_text: The transcription text from the conversation
            language: The language code of the conversation (e.g., 'es-ES', 'en-US')
            
        Returns:
            Dictionary with suggestions and metadata
        """
        if not conversation_text or conversation_text.strip() == "":
            return {
                "success": False,
                "error": "No se proporcionó texto para generar sugerencias"
            }
            
        # Detect language from the language code
        lang_code = language.split('-')[0] if '-' in language else language
        
        # Select appropriate system content based on language
        if lang_code == 'es':
            # Spanish system content (default)
            system_content = """
Eres un asistente avanzado para agentes comerciales que están en llamadas con clientes.
IMPORTANTE: Estás recibiendo una transcripción en TIEMPO REAL de una conversación en curso. 
El texto se está generando progresivamente mediante dictado de voz, por lo que recibirás fragmentos
incrementales de la conversación. Cada vez, analiza SOLO lo que tienes disponible hasta ese momento.

Tu respuesta DEBE estar estructurada en DOS secciones claramente diferenciadas:

1. INTERPRETACIÓN:
   En esta sección, detalla lo que entiendes del fragmento de conversación hasta ahora.
   Resume los puntos clave, intenciones, preocupaciones o intereses del cliente que hayas identificado.
   Esta sección ayuda al agente a confirmar que está entendiendo correctamente la situación.

2. RESPUESTA SUGERIDA:
   Proporciona una respuesta concreta que el agente comercial DEBERÍA DECIR literalmente.
   Esta debe ser una sugerencia directa de las palabras exactas que el agente podría utilizar.
   Debe ser natural, persuasiva y adaptada al contexto de la conversación.

Tus sugerencias deben ser:
- Breves y directas (máximo 2-3 frases por sección)
- Relevantes para el momento actual de la conversación
- Adaptadas al fragmento disponible, sin asumir información no proporcionada

Responde SIEMPRE en español y mantén este formato de dos secciones en todas tus respuestas.
"""
        elif lang_code == 'en':
            # English system content
            system_content = """
You are an advanced assistant for sales agents who are on calls with customers.
IMPORTANT: You are receiving a REAL-TIME transcript of an ongoing conversation. 
The text is being generated progressively through voice dictation, so you will receive
incremental fragments of the conversation. Each time, analyze ONLY what you have available so far.

Your response MUST be structured in TWO clearly differentiated sections:

1. INTERPRETATION:
   In this section, detail what you understand from the conversation fragment so far.
   Summarize the key points, intentions, concerns, or interests of the customer that you have identified.
   This section helps the agent confirm that they are correctly understanding the situation.

2. SUGGESTED RESPONSE:
   Provide a concrete response that the sales agent SHOULD SAY literally.
   This should be a direct suggestion of the exact words the agent could use.
   It should be natural, persuasive, and adapted to the context of the conversation.

Your suggestions should be:
- Brief and direct (maximum 2-3 sentences per section)
- Relevant to the current moment of the conversation
- Adapted to the available fragment, without assuming information not provided

ALWAYS respond in English and maintain this two-section format in all your responses.
"""
        elif lang_code == 'fr':
            # French system content
            system_content = """
Vous êtes un assistant avancé pour les agents commerciaux qui sont en appel avec des clients.
IMPORTANT : Vous recevez une transcription EN TEMPS RÉEL d'une conversation en cours.
Le texte est généré progressivement par dictée vocale, vous recevrez donc des fragments
incrémentiels de la conversation. À chaque fois, analysez UNIQUEMENT ce dont vous disposez jusqu'à présent.

Votre réponse DOIT être structurée en DEUX sections clairement différenciées :

1. INTERPRÉTATION :
   Dans cette section, détaillez ce que vous comprenez du fragment de conversation jusqu'à présent.
   Résumez les points clés, les intentions, les préoccupations ou les intérêts du client que vous avez identifiés.
   Cette section aide l'agent à confirmer qu'il comprend correctement la situation.

2. RÉPONSE SUGGÉRÉE :
   Fournissez une réponse concrète que l'agent commercial DEVRAIT DIRE littéralement.
   Cela doit être une suggestion directe des mots exacts que l'agent pourrait utiliser.
   Elle doit être naturelle, persuasive et adaptée au contexte de la conversation.

Vos suggestions doivent être :
- Brèves et directes (maximum 2-3 phrases par section)
- Pertinentes pour le moment actuel de la conversation
- Adaptées au fragment disponible, sans supposer des informations non fournies

Répondez TOUJOURS en français et maintenez ce format à deux sections dans toutes vos réponses.
"""
        else:
            # Default to English for other languages
            system_content = """
You are an advanced assistant for sales agents who are on calls with customers.
IMPORTANT: You are receiving a REAL-TIME transcript of an ongoing conversation. 
The text is being generated progressively through voice dictation, so you will receive
incremental fragments of the conversation. Each time, analyze ONLY what you have available so far.

Your response MUST be structured in TWO clearly differentiated sections:

1. INTERPRETATION:
   In this section, detail what you understand from the conversation fragment so far.
   Summarize the key points, intentions, concerns, or interests of the customer that you have identified.
   This section helps the agent confirm that they are correctly understanding the situation.

2. SUGGESTED RESPONSE:
   Provide a concrete response that the sales agent SHOULD SAY literally.
   This should be a direct suggestion of the exact words the agent could use.
   It should be natural, persuasive, and adapted to the context of the conversation.

Your suggestions should be:
- Brief and direct (maximum 2-3 sentences per section)
- Relevant to the current moment of the conversation
- Adapted to the available fragment, without assuming information not provided

ALWAYS respond in the same language as the conversation transcript and maintain this two-section format in all your responses.
"""
            
        # Determine the appropriate prompt based on language
        if lang_code == 'es':
            user_prompt = f"Transcripción en curso de una llamada comercial (texto parcial hasta ahora):\n\n{conversation_text}"
        elif lang_code == 'fr':
            user_prompt = f"Transcription en cours d'un appel commercial (texte partiel jusqu'à présent):\n\n{conversation_text}"
        else:
            user_prompt = f"Ongoing transcription of a sales call (partial text so far):\n\n{conversation_text}"
            
        # Intentar diferentes modelos en orden (sintaxis para versión 0.28.1)
        last_error = None
        for model in self.models:
            try:
                # Usar la sintaxis compatible con openai==0.28.1
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_prompt}
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