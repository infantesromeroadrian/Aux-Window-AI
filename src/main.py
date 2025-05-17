from flask import Flask, render_template, request, jsonify, session
import os
import logging
import uuid
from datetime import datetime
from dotenv import load_dotenv
from services.openai_service import OpenAIService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
    static_folder='static',
    template_folder='templates'
)
app.secret_key = os.getenv("SECRET_KEY", "sandetel_rag_solution_secret")

# Almacenamiento para las sesiones de conversación
conversation_sessions = {}

# Initialize services
openai_service = None
try:
    openai_service = OpenAIService()
    logger.info("OpenAI service initialized successfully")
except ValueError as e:
    logger.warning(f"OpenAI service initialization failed: {e}")
    logger.warning("The application will run without OpenAI integration")

@app.route('/')
def index():
    """Render the main page of the application."""
    # Crear una nueva sesión si no existe
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversation_sessions[session['session_id']] = {
            'transcript': '',
            'start_time': session['start_time'],
            'client_info': {}
        }
    
    return render_template('index.html', 
                          session_id=session['session_id'],
                          start_time=session['start_time'])

@app.route('/new-session', methods=['POST'])
def new_session():
    """Create a new conversation session."""
    # Guardar la sesión actual si existe
    old_session_id = session.get('session_id')
    if old_session_id:
        logger.info(f"Storing previous session: {old_session_id}")
        # Aquí podríamos guardar la sesión en una base de datos permanente
    
    # Crear nueva sesión
    session['session_id'] = str(uuid.uuid4())
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conversation_sessions[session['session_id']] = {
        'transcript': '',
        'start_time': session['start_time'],
        'client_info': {}
    }
    
    logger.info(f"Created new session: {session['session_id']}")
    return jsonify({
        'success': True,
        'session_id': session['session_id'],
        'start_time': session['start_time']
    })

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Endpoint to handle real-time transcription requests."""
    # This will be implemented later to handle speech-to-text
    # For now, we're just returning a mock response
    return jsonify({'success': True, 'text': 'Mock transcription'})

@app.route('/update-transcript', methods=['POST'])
def update_transcript():
    """Update the stored transcript for the current session."""
    session_id = session.get('session_id')
    if not session_id or session_id not in conversation_sessions:
        logger.warning("Session ID not found when updating transcript")
        return jsonify({
            'success': False,
            'error': 'Sesión no encontrada'
        })
        
    text = request.json.get('text', '')
    conversation_sessions[session_id]['transcript'] = text
    
    logger.info(f"Updated transcript for session {session_id}")
    return jsonify({
        'success': True
    })

@app.route('/get-suggestions', methods=['POST'])
def get_suggestions():
    """Endpoint to get suggestions from the LLM based on transcribed text."""
    text = request.json.get('text', '')
    language = request.json.get('language', 'es-ES')  # Default to Spanish if not specified
    
    # Actualizar la transcripción almacenada
    session_id = session.get('session_id')
    if session_id and session_id in conversation_sessions:
        conversation_sessions[session_id]['transcript'] = text
    
    if not text:
        logger.warning("No text provided for suggestions")
        return jsonify({
            'success': False,
            'error': 'No text provided'
        })
    
    if openai_service:
        logger.info(f"Getting suggestions for text: {text[:50]}... in language: {language}")
        result = openai_service.get_suggestions(text, language)
        if not result.get('success'):
            logger.error(f"Error getting suggestions: {result.get('error')}")
        else:
            logger.info(f"Successfully got suggestions using model: {result.get('model')}")
        return jsonify(result)
    else:
        # Fallback if OpenAI service is not available
        logger.warning("Using fallback suggestions (OpenAI service not available)")
        return jsonify({
            'success': True,
            'suggestions': f'⚠️ [MODO DEMO] Sugerencia basada en: {text[:50]}... Para obtener sugerencias reales, configura la API de OpenAI.'
        })

@app.route('/ask-question', methods=['POST'])
def ask_question():
    """Endpoint to get answers to direct questions from the LLM."""
    question = request.json.get('question', '')
    
    if not question:
        logger.warning("No question provided")
        return jsonify({
            'success': False,
            'error': 'No se ha proporcionado ninguna pregunta'
        })
    
    if openai_service:
        logger.info(f"Processing question: {question[:50]}...")
        try:
            result = openai_service.get_answer_to_question(question)
            if not result.get('success'):
                logger.error(f"Error getting answer: {result.get('error')}")
            else:
                logger.info(f"Successfully got answer using model: {result.get('model')}")
            return jsonify(result)
        except Exception as e:
            logger.error(f"Exception processing question: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al procesar la pregunta: {str(e)}'
            })
    else:
        # Fallback if OpenAI service is not available
        logger.warning("Using fallback answer (OpenAI service not available)")
        return jsonify({
            'success': True,
            'answer': f'⚠️ [MODO DEMO] Respuesta a tu pregunta: "{question}". Para obtener respuestas reales, configura la API de OpenAI.'
        })

@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    """Endpoint to analyze customer sentiment from conversation text."""
    text = request.json.get('text', '')
    
    if not text:
        logger.warning("No text provided for sentiment analysis")
        return jsonify({
            'success': False,
            'error': 'No se ha proporcionado texto para análisis'
        })
    
    if openai_service:
        logger.info(f"Analyzing sentiment for text: {text[:50]}...")
        try:
            result = openai_service.analyze_sentiment(text)
            if not result.get('success'):
                logger.error(f"Error analyzing sentiment: {result.get('error')}")
            else:
                logger.info(f"Successfully analyzed sentiment using model: {result.get('model')}")
            return jsonify(result)
        except Exception as e:
            logger.error(f"Exception analyzing sentiment: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al analizar el sentimiento: {str(e)}'
            })
    else:
        # Fallback if OpenAI service is not available
        logger.warning("Using fallback sentiment analysis (OpenAI service not available)")
        return jsonify({
            'success': True,
            'sentiment_analysis': f'⚠️ [MODO DEMO] Análisis de sentimiento para el texto proporcionado. Configure la API de OpenAI para análisis real.'
        })

@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    """Endpoint to generate a call summary from conversation text."""
    text = request.json.get('text', '')
    session_id = session.get('session_id')
    
    # Si no se proporciona texto, usar la transcripción almacenada para la sesión
    if not text and session_id and session_id in conversation_sessions:
        text = conversation_sessions[session_id].get('transcript', '')
    
    if not text:
        logger.warning("No text provided for summary generation")
        return jsonify({
            'success': False,
            'error': 'No hay texto de conversación para resumir'
        })
    
    if openai_service:
        logger.info(f"Generating summary for text: {text[:50]}...")
        try:
            result = openai_service.generate_call_summary(text)
            if not result.get('success'):
                logger.error(f"Error generating summary: {result.get('error')}")
            else:
                logger.info(f"Successfully generated summary using model: {result.get('model')}")
                
                # Guardar el resumen en la sesión
                if session_id and session_id in conversation_sessions:
                    conversation_sessions[session_id]['summary'] = result.get('call_summary')
                    
            return jsonify(result)
        except Exception as e:
            logger.error(f"Exception generating summary: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al generar el resumen: {str(e)}'
            })
    else:
        # Fallback if OpenAI service is not available
        logger.warning("Using fallback summary generation (OpenAI service not available)")
        return jsonify({
            'success': True,
            'call_summary': f'⚠️ [MODO DEMO] Resumen de la llamada. Configure la API de OpenAI para resúmenes reales.'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True) 