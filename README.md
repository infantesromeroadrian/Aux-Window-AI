# Conversation Transcription System

A Flask-based web application that allows real-time transcription and recording of conversations between agents and clients.

## Features

- Real-time conversation transcription using WebSockets
- Audio recording and speech-to-text conversion
- Multiple transcription service options (Browser API, Google Speech-to-Text, OpenAI Whisper)
- Ability to switch between agent and client perspectives
- Persistent storage of conversations
- Export functionality for transcripts
- Mobile-friendly responsive design

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **Models**: Define data structures for conversations and messages
- **Services**: Handle business logic, data persistence, and transcription services
- **Controllers**: Manage HTTP and WebSocket routes
- **Templates**: Render the user interface
- **Static Files**: CSS styles and client-side JavaScript

## Tech Stack

- **Backend**: Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: File-based JSON storage
- **Speech-to-Text**: Web Speech API, Google Speech-to-Text, OpenAI Whisper
- **Containerization**: Docker with Docker Compose

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- (Optional) API keys for transcription services:
  - Google Cloud Speech-to-Text API key
  - OpenAI API key for Whisper

### Running the Application

1. Clone this repository
2. Navigate to the project directory
3. (Optional) Configure your API keys in docker-compose.yml
4. Run the application using Docker Compose:

```bash
docker-compose up --build
```

5. Access the application at http://localhost:8501

## Configuration

The application can be configured using environment variables in the docker-compose.yml file:

- `TRANSCRIPTION_SERVICE`: The transcription service to use (`speechrecognition`, `google`, `whisper`)
- `LANGUAGE_CODE`: The language code for transcription (default: `es-ES`)
- `OPENAI_API_KEY`: Your OpenAI API key for Whisper (if using Whisper)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud credentials file (if using Google Speech-to-Text)

## Development

### Project Structure

```
Sandetel-RAG-Solution/
├── src/
│   ├── models/
│   │   └── conversation.py
│   ├── utils/
│   │   ├── config.py
│   │   └── helpers.py
│   ├── services/
│   │   ├── conversation_service.py
│   │   └── transcription_service.py
│   ├── controllers/
│   │   └── transcription_controller.py
│   └── main.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── index.html
│   └── conversation.html
├── data/
│   └── conversations/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

### Speech-to-Text Options

The application supports three options for speech-to-text conversion:

1. **SpeechRecognition**: Uses the Web Speech API in the browser or the `SpeechRecognition` Python library on the server.
2. **Google Speech-to-Text**: Uses Google's Cloud Speech-to-Text API for high-quality transcription.
3. **OpenAI Whisper**: Uses OpenAI's powerful Whisper model for transcription.

To configure a different service, set the `TRANSCRIPTION_SERVICE` environment variable in docker-compose.yml.

### Running Tests

```bash
docker-compose run transcription-app python -m pytest
```

## License

This project is licensed under the MIT License. 