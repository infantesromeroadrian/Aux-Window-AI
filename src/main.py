from flask import Flask, render_template, request, jsonify
import os
import logging
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
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Endpoint to handle real-time transcription requests."""
    # This will be implemented later to handle speech-to-text
    # For now, we're just returning a mock response
    return jsonify({'success': True, 'text': 'Mock transcription'})

@app.route('/get-suggestions', methods=['POST'])
def get_suggestions():
    """Endpoint to get suggestions from the LLM based on transcribed text."""
    text = request.json.get('text', '')
    
    if not text:
        logger.warning("No text provided for suggestions")
        return jsonify({
            'success': False,
            'error': 'No text provided'
        })
    
    if openai_service:
        logger.info(f"Getting suggestions for text: {text[:50]}...")
        result = openai_service.get_suggestions(text)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True) 