import os
import tempfile
import speech_recognition as sr
from abc import ABC, abstractmethod
import openai
from google.cloud import speech
import io
from pydub import AudioSegment


class TranscriptionService(ABC):
    """Base class for transcription services."""
    
    @abstractmethod
    def transcribe(self, audio_data):
        """Transcribe audio data to text.
        
        Args:
            audio_data: Binary audio data
            
        Returns:
            Transcribed text
        """
        pass


class GoogleTranscriptionService(TranscriptionService):
    """Google Speech-to-Text API service."""
    
    def __init__(self, language_code='es-ES'):
        """Initialize the Google Speech-to-Text client.
        
        Args:
            language_code: Language code for transcription
        """
        self.client = speech.SpeechClient()
        self.language_code = language_code
        
    def transcribe(self, audio_data):
        """Transcribe audio using Google Speech-to-Text.
        
        Args:
            audio_data: Binary audio data
            
        Returns:
            Transcribed text
        """
        try:
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=self.language_code,
                enable_automatic_punctuation=True
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript
                
            return transcript
        except Exception as e:
            print(f"Error in Google transcription: {e}")
            return ""


class WhisperTranscriptionService(TranscriptionService):
    """OpenAI Whisper API service."""
    
    def __init__(self, api_key=None, language='es'):
        """Initialize the Whisper service.
        
        Args:
            api_key: OpenAI API key
            language: Language for transcription
        """
        if api_key:
            openai.api_key = api_key
        else:
            openai.api_key = os.environ.get('OPENAI_API_KEY', '')
        self.language = language
        
    def transcribe(self, audio_data):
        """Transcribe audio using Whisper.
        
        Args:
            audio_data: Binary audio data
            
        Returns:
            Transcribed text
        """
        try:
            # Save audio data to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            with open(temp_audio_path, 'rb') as audio_file:
                transcript = openai.Audio.transcribe(
                    "whisper-1",
                    audio_file,
                    language=self.language
                )
            
            # Clean up the temporary file
            os.unlink(temp_audio_path)
            
            return transcript.get('text', '')
        except Exception as e:
            print(f"Error in Whisper transcription: {e}")
            return ""


class SpeechRecognitionService(TranscriptionService):
    """Use the SpeechRecognition library with various backends."""
    
    def __init__(self, service='google', language='es-ES'):
        """Initialize the speech recognition service.
        
        Args:
            service: Service to use ('google', 'sphinx', 'wit', 'bing', 'azure', 'houndify')
            language: Language code for transcription
        """
        self.recognizer = sr.Recognizer()
        self.service = service
        self.language = language
        
    def transcribe(self, audio_data):
        """Transcribe audio using the selected service.
        
        Args:
            audio_data: Binary audio data
            
        Returns:
            Transcribed text
        """
        try:
            # Save audio data to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            # Convert to AudioData object
            with sr.AudioFile(temp_audio_path) as source:
                audio = self.recognizer.record(source)
            
            # Clean up the temporary file
            os.unlink(temp_audio_path)
            
            # Transcribe using the selected service
            transcript = ""
            if self.service == 'google':
                transcript = self.recognizer.recognize_google(audio, language=self.language)
            elif self.service == 'sphinx':
                transcript = self.recognizer.recognize_sphinx(audio, language=self.language)
            elif self.service == 'wit':
                transcript = self.recognizer.recognize_wit(audio, key=os.environ.get('WIT_AI_KEY', ''))
            elif self.service == 'bing':
                transcript = self.recognizer.recognize_bing(audio, key=os.environ.get('BING_KEY', ''), language=self.language)
            elif self.service == 'azure':
                transcript = self.recognizer.recognize_azure(audio, key=os.environ.get('AZURE_SPEECH_KEY', ''), location=os.environ.get('AZURE_SPEECH_LOCATION', ''), language=self.language)
            elif self.service == 'houndify':
                transcript = self.recognizer.recognize_houndify(audio, client_id=os.environ.get('HOUNDIFY_CLIENT_ID', ''), client_key=os.environ.get('HOUNDIFY_CLIENT_KEY', ''))
            
            return transcript
        except Exception as e:
            print(f"Error in SpeechRecognition transcription: {e}")
            return ""


def get_transcription_service(service_type='speechrecognition', **kwargs):
    """Factory function to get a transcription service.
    
    Args:
        service_type: Type of service ('google', 'whisper', 'speechrecognition')
        **kwargs: Additional arguments for the service
        
    Returns:
        TranscriptionService instance
    """
    if service_type == 'google':
        return GoogleTranscriptionService(**kwargs)
    elif service_type == 'whisper':
        return WhisperTranscriptionService(**kwargs)
    else:
        return SpeechRecognitionService(**kwargs) 