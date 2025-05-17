// Variables for speech recognition
let recognition;
let recognitionActive = false;
let transcriptionText = '';
let suggestionsDebounceTimer;
let sentimentDebounceTimer;
let currentLanguage = 'es-ES'; // Default language

// DOM elements for speech recognition
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const resetButton = document.getElementById('resetButton');
const liveTranscription = document.getElementById('liveTranscription');
const liveSuggestions = document.getElementById('liveSuggestions');
const transcriptionBox = document.getElementById('transcriptionBox');
const loadingSpinner = document.getElementById('loadingSpinner');
const languageSelector = document.getElementById('languageSelector');
const languageMenu = document.getElementById('languageMenu');

// DOM elements for direct questions
const questionForm = document.getElementById('questionForm');
const questionInput = document.getElementById('questionInput');
const assistantAnswer = document.getElementById('assistantAnswer');
const questionLoadingSpinner = document.getElementById('questionLoadingSpinner');

// DOM elements for sentiment analysis and call summary
const analyzeSentimentBtn = document.getElementById('analyzeSentimentBtn');
const sentimentAnalysis = document.getElementById('sentimentAnalysis');
const sentimentLoadingSpinner = document.getElementById('sentimentLoadingSpinner');
const generateSummaryBtn = document.getElementById('generateSummaryBtn');
const callSummary = document.getElementById('callSummary');
const summaryLoadingSpinner = document.getElementById('summaryLoadingSpinner');

// DOM elements for session management
const newSessionBtn = document.getElementById('newSessionBtn');
const sessionId = document.getElementById('sessionId');
const sessionTime = document.getElementById('sessionTime');
const newSessionModal = new bootstrap.Modal(document.getElementById('newSessionModal'));
const confirmNewSession = document.getElementById('confirmNewSession');

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
    recognition.lang = currentLanguage;
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
            updateTranscript(transcriptionText);
            getSuggestions(transcriptionText);
            getStreamingSentimentAnalysis(transcriptionText);
        } else {
            // Show interim results in real-time
            const interimText = transcriptionText + ' ' + transcript;
            liveTranscription.textContent = interimText;
            
            // Debounce suggestions requests for interim results
            clearTimeout(suggestionsDebounceTimer);
            suggestionsDebounceTimer = setTimeout(() => {
                getSuggestions(interimText);
            }, 1000);
            
            // Debounce sentiment analysis for interim results
            clearTimeout(sentimentDebounceTimer);
            sentimentDebounceTimer = setTimeout(() => {
                getStreamingSentimentAnalysis(interimText);
            }, 1500); // Slightly longer debounce for sentiment to avoid too many calls
        }
    };
    
    return true;
}

// Setup language selector
function setupLanguageSelector() {
    // Add click event listener to language menu items
    if (languageMenu) {
        const languageItems = languageMenu.querySelectorAll('.dropdown-item');
        languageItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Get the language code
                const lang = this.getAttribute('data-lang');
                currentLanguage = lang;
                
                // Update the button text
                languageSelector.innerHTML = `<i class="bi bi-globe"></i> ${this.textContent}`;
                
                // Set active class
                languageItems.forEach(li => li.classList.remove('active'));
                this.classList.add('active');
                
                // If recognition is active, restart it with the new language
                if (recognitionActive) {
                    stopRecognition();
                    startRecognition();
                }
            });
        });
    }
}

// Start voice recognition
function startRecognition() {
    if (!recognition && !initSpeechRecognition()) {
        return;
    }
    
    // Set the current language
    recognition.lang = currentLanguage;
    
    recognitionActive = true;
    recognition.start();
    
    // Update UI to show that streaming analysis is active
    document.getElementById('analyzeSentimentBtn').setAttribute('disabled', 'disabled');
    document.getElementById('sentimentStatusIndicator').classList.remove('d-none');
}

// Stop voice recognition
function stopRecognition() {
    if (recognition) {
        recognitionActive = false;
        recognition.stop();
        updateUI(false);
        
        // Re-enable manual analysis button
        document.getElementById('analyzeSentimentBtn').removeAttribute('disabled');
        document.getElementById('sentimentStatusIndicator').classList.add('d-none');
    }
}

// Reset transcription and suggestions
function resetAll() {
    transcriptionText = '';
    liveTranscription.textContent = 'La transcripción aparecerá aquí en tiempo real...';
    liveSuggestions.textContent = 'Las sugerencias aparecerán aquí mientras hablas...';
    sentimentAnalysis.textContent = 'El análisis de sentimiento aparecerá aquí...';
    callSummary.textContent = 'El resumen de la llamada aparecerá aquí...';
    
    updateTranscript('');
    
    if (recognitionActive) {
        stopRecognition();
    }
}

// Update the stored transcript on the server
function updateTranscript(text) {
    fetch('/update-transcript', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error updating transcript:', error);
    });
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
        body: JSON.stringify({ 
            text: text,
            language: currentLanguage 
        })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        loadingSpinner.classList.add('d-none');
        
        if (data.success) {
            // Format the suggestions content
            liveSuggestions.innerHTML = data.suggestions.replace(/\n/g, '<br>');
        } else {
            liveSuggestions.textContent = `Error: ${data.error || 'No se pudieron obtener sugerencias.'}`;
        }
    })
    .catch(error => {
        console.error('Error getting suggestions:', error);
        loadingSpinner.classList.add('d-none');
        liveSuggestions.textContent = 'Error de conexión al obtener sugerencias.';
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

// Get streaming sentiment analysis
function getStreamingSentimentAnalysis(text) {
    if (!text || text.trim() === '') return;
    
    // Show loading spinner
    sentimentLoadingSpinner.classList.remove('d-none');
    
    fetch('/analyze-sentiment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        sentimentLoadingSpinner.classList.add('d-none');
        
        if (data.success && data.sentiment_analysis) {
            sentimentAnalysis.textContent = data.sentiment_analysis;
        } else if (data.error) {
            console.error('Error analyzing sentiment:', data.error);
            sentimentAnalysis.textContent = `Error: ${data.error}`;
        } else {
            console.error('Unknown error analyzing sentiment:', data);
            sentimentAnalysis.textContent = 'No se pudo analizar el sentimiento. Verifica la configuración de la API.';
        }
    })
    .catch(error => {
        // Hide loading spinner
        sentimentLoadingSpinner.classList.add('d-none');
        console.error('Error:', error);
        sentimentAnalysis.textContent = 'Error de conexión. Inténtalo de nuevo.';
    });
}

// Analyze sentiment from the conversation (manual trigger)
function analyzeSentiment() {
    if (!transcriptionText || transcriptionText.trim() === '') {
        sentimentAnalysis.textContent = 'No hay texto para analizar. Inicia el dictado primero.';
        return;
    }
    
    getStreamingSentimentAnalysis(transcriptionText);
}

// Generate call summary
function generateSummary() {
    if (!transcriptionText || transcriptionText.trim() === '') {
        callSummary.textContent = 'No hay texto para resumir. Inicia el dictado primero.';
        return;
    }
    
    // Show loading spinner
    summaryLoadingSpinner.classList.remove('d-none');
    
    fetch('/generate-summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: transcriptionText })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        summaryLoadingSpinner.classList.add('d-none');
        
        if (data.success && data.call_summary) {
            callSummary.textContent = data.call_summary;
        } else if (data.error) {
            console.error('Error generating summary:', data.error);
            callSummary.textContent = `Error: ${data.error}`;
        } else {
            console.error('Unknown error generating summary:', data);
            callSummary.textContent = 'No se pudo generar el resumen. Verifica la configuración de la API.';
        }
    })
    .catch(error => {
        // Hide loading spinner
        summaryLoadingSpinner.classList.add('d-none');
        console.error('Error:', error);
        callSummary.textContent = 'Error de conexión. Inténtalo de nuevo.';
    });
}

// Start new session
function startNewSession() {
    fetch('/new-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update session info in UI
            sessionId.textContent = data.session_id;
            sessionTime.textContent = data.start_time;
            
            // Reset all fields
            resetAll();
            
            // Close modal
            newSessionModal.hide();
        } else {
            console.error('Error creating new session:', data.error);
            alert('Error al crear nueva sesión: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error de conexión al crear nueva sesión');
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
    
    // Setup language selector
    setupLanguageSelector();
    
    // Form submission for direct questions
    questionForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const question = questionInput.value.trim();
        if (question) {
            askQuestion(question);
            questionInput.value = '';
        }
    });
    
    // Button event listeners for sentiment analysis and call summary
    analyzeSentimentBtn.addEventListener('click', analyzeSentiment);
    generateSummaryBtn.addEventListener('click', generateSummary);
    
    // Button event listeners for session management
    newSessionBtn.addEventListener('click', function() {
        newSessionModal.show();
    });
    
    confirmNewSession.addEventListener('click', startNewSession);
}); 