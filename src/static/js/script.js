// Variables for speech recognition
let recognition;
let recognitionActive = false;
let transcriptionText = '';
let suggestionsDebounceTimer;

// DOM elements
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const resetButton = document.getElementById('resetButton');
const liveTranscription = document.getElementById('liveTranscription');
const liveSuggestions = document.getElementById('liveSuggestions');
const transcriptionBox = document.getElementById('transcriptionBox');
const loadingSpinner = document.getElementById('loadingSpinner');

// DOM elements for direct questions
const questionForm = document.getElementById('questionForm');
const questionInput = document.getElementById('questionInput');
const assistantAnswer = document.getElementById('assistantAnswer');
const questionLoadingSpinner = document.getElementById('questionLoadingSpinner');

// Initialize speech recognition
function initSpeechRecognition() {
    // Check browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Tu navegador no soporta el reconocimiento de voz. Por favor, usa Chrome, Edge o Safari.');
        return false;
    }

    // Create speech recognition instance
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    
    // Configure recognition
    recognition.lang = 'es-ES';
    recognition.continuous = true;
    recognition.interimResults = true;
    
    // Event handlers
    recognition.onstart = function() {
        recognitionActive = true;
        updateUI(true);
    };
    
    recognition.onend = function() {
        if (recognitionActive) {
            // Restart if it was still active (to make it continuous)
            recognition.start();
        }
    };
    
    recognition.onerror = function(event) {
        console.error('Error de reconocimiento de voz:', event.error);
        if (event.error === 'no-speech') {
            // This is not a fatal error, just restart
            if (recognitionActive) {
                recognition.start();
            }
        } else {
            recognitionActive = false;
            updateUI(false);
            alert('Error en el reconocimiento de voz: ' + event.error);
        }
    };
    
    recognition.onresult = function(event) {
        // Get the latest result
        const result = event.results[event.results.length - 1];
        const transcript = result[0].transcript;
        
        // Update the transcription text
        if (result.isFinal) {
            transcriptionText += ' ' + transcript;
            liveTranscription.textContent = transcriptionText;
            getSuggestions(transcriptionText);
        } else {
            // Show interim results in real-time
            liveTranscription.textContent = transcriptionText + ' ' + transcript;
            
            // Debounce suggestions requests for interim results
            clearTimeout(suggestionsDebounceTimer);
            suggestionsDebounceTimer = setTimeout(() => {
                getSuggestions(transcriptionText + ' ' + transcript);
            }, 1000);
        }
    };
    
    return true;
}

// Start voice recognition
function startRecognition() {
    if (!recognition && !initSpeechRecognition()) {
        return;
    }
    
    recognitionActive = true;
    recognition.start();
}

// Stop voice recognition
function stopRecognition() {
    if (recognition) {
        recognitionActive = false;
        recognition.stop();
        updateUI(false);
    }
}

// Reset transcription and suggestions
function resetAll() {
    transcriptionText = '';
    liveTranscription.textContent = 'La transcripción aparecerá aquí en tiempo real...';
    liveSuggestions.textContent = 'Las sugerencias aparecerán aquí mientras hablas...';
    
    if (recognitionActive) {
        stopRecognition();
    }
}

// Update UI based on recognition state
function updateUI(isRecording) {
    if (isRecording) {
        startButton.disabled = true;
        stopButton.disabled = false;
        transcriptionBox.classList.add('recording');
    } else {
        startButton.disabled = false;
        stopButton.disabled = true;
        transcriptionBox.classList.remove('recording');
    }
}

// Get suggestions from the server based on transcription
function getSuggestions(text) {
    if (!text || text.trim() === '') return;
    
    // Show loading spinner
    loadingSpinner.classList.remove('d-none');
    
    fetch('/get-suggestions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        loadingSpinner.classList.add('d-none');
        
        if (data.success && data.suggestions) {
            liveSuggestions.textContent = data.suggestions;
        } else if (data.error) {
            console.error('Error getting suggestions:', data.error);
            liveSuggestions.textContent = `Error: ${data.error}`;
        } else {
            console.error('Unknown error getting suggestions:', data);
            liveSuggestions.textContent = 'No se pudieron obtener sugerencias. Verifica la configuración de la API.';
        }
    })
    .catch(error => {
        // Hide loading spinner
        loadingSpinner.classList.add('d-none');
        console.error('Error:', error);
        liveSuggestions.textContent = 'Error de conexión. Inténtalo de nuevo.';
    });
}

// Get answer for a direct question
function askQuestion(question) {
    if (!question || question.trim() === '') {
        assistantAnswer.textContent = 'Por favor, escribe una pregunta.';
        return;
    }
    
    // Show loading spinner
    questionLoadingSpinner.classList.remove('d-none');
    
    // Disable form while processing
    questionInput.disabled = true;
    
    fetch('/ask-question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner and enable form
        questionLoadingSpinner.classList.add('d-none');
        questionInput.disabled = false;
        questionInput.focus();
        
        if (data.success && data.answer) {
            assistantAnswer.textContent = data.answer;
        } else if (data.error) {
            console.error('Error getting answer:', data.error);
            assistantAnswer.textContent = `Error: ${data.error}`;
        } else {
            console.error('Unknown error getting answer:', data);
            assistantAnswer.textContent = 'No se pudo obtener una respuesta. Verifica la configuración de la API.';
        }
    })
    .catch(error => {
        // Hide loading spinner and enable form
        questionLoadingSpinner.classList.add('d-none');
        questionInput.disabled = false;
        questionInput.focus();
        
        console.error('Error:', error);
        assistantAnswer.textContent = 'Error de conexión. Inténtalo de nuevo.';
    });
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize speech recognition
    initSpeechRecognition();
    
    // Button event listeners for speech recognition
    startButton.addEventListener('click', startRecognition);
    stopButton.addEventListener('click', stopRecognition);
    resetButton.addEventListener('click', resetAll);
    
    // Form submission for direct questions
    questionForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const question = questionInput.value;
        askQuestion(question);
        // Clear input field after submission
        questionInput.value = '';
    });
}); 