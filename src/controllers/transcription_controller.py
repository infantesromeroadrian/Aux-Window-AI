from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import os
import base64

from services.conversation_service import ConversationService
from services.transcription_service import get_transcription_service


def register_transcription_routes(app: Flask, socketio: SocketIO):
    """Register routes for the transcription feature.
    
    Args:
        app: Flask application instance
        socketio: SocketIO instance
    """
    conversation_service = ConversationService()
    # Initialize the transcription service based on environment variables
    transcription_service_type = os.environ.get('TRANSCRIPTION_SERVICE', 'speechrecognition')
    transcription_service = get_transcription_service(
        service_type=transcription_service_type,
        language=os.environ.get('LANGUAGE_CODE', 'es-ES')
    )
    
    @app.route('/')
    def index():
        """Render the main page with conversation list."""
        conversations = conversation_service.list_conversations()
        return render_template('index.html', conversations=conversations)
    
    @app.route('/conversations/new', methods=['POST'])
    def create_conversation():
        """Create a new conversation and redirect to it."""
        conversation = conversation_service.create_conversation()
        # Save the conversation to disk to prevent redirect loops
        conversation_service._save_conversation(conversation)
        return redirect(url_for('view_conversation', conversation_id=conversation.id))
    
    @app.route('/conversations/<conversation_id>')
    def view_conversation(conversation_id):
        """Render the conversation view page.
        
        Args:
            conversation_id: ID of the conversation to view
        """
        conversation = conversation_service.get_conversation(conversation_id)
        if not conversation:
            # Create new conversation and save it before redirecting
            conversation = conversation_service.create_conversation()
            conversation_service._save_conversation(conversation)
            return redirect(url_for('view_conversation', conversation_id=conversation.id))
            
        return render_template(
            'conversation.html',
            conversation=conversation.to_dict(),
            conversation_id=conversation_id,
            transcription_service=transcription_service_type
        )
    
    @app.route('/api/conversations/<conversation_id>/messages', methods=['POST'])
    def add_message(conversation_id):
        """Add a message to a conversation via HTTP.
        
        Args:
            conversation_id: ID of the conversation
        """
        data = request.json
        sender = data.get('sender')
        content = data.get('content')
        client_message_id = data.get('client_message_id')
        
        if not sender or not content:
            return jsonify({
                'error': 'Sender and content are required'
            }), 400
            
        message = conversation_service.add_message(conversation_id, sender, content)
        if not message:
            return jsonify({
                'error': 'Conversation not found'
            }), 404
            
        # Broadcast the message to all clients in the room
        message_data = message.to_dict()
        if client_message_id:
            message_data['client_message_id'] = client_message_id
            
        socketio.emit(
            'new_message',
            message_data,
            room=conversation_id
        )
            
        return jsonify(message.to_dict()), 201
    
    @app.route('/api/transcribe', methods=['POST'])
    def transcribe_audio():
        """Transcribe audio to text.
        
        Expects:
            audio_data: Base64 encoded audio data
            
        Returns:
            JSON with transcribed text
        """
        data = request.json
        audio_base64 = data.get('audio_data', '')
        
        if not audio_base64:
            return jsonify({
                'error': 'Audio data is required'
            }), 400
            
        try:
            # Decode base64 audio data
            audio_data = base64.b64decode(audio_base64.split(',')[1])
            
            # Transcribe audio
            text = transcription_service.transcribe(audio_data)
            
            return jsonify({
                'text': text
            })
        except Exception as e:
            return jsonify({
                'error': f'Transcription failed: {str(e)}'
            }), 500
    
    @socketio.on('join')
    def on_join(data):
        """Join a conversation room.
        
        Args:
            data: Dictionary containing the conversation_id
        """
        conversation_id = data.get('conversation_id')
        if conversation_id:
            from flask_socketio import join_room
            join_room(conversation_id)
            emit('status', {'msg': f'Joined conversation {conversation_id}'}, room=conversation_id)
    
    @socketio.on('leave')
    def on_leave(data):
        """Leave a conversation room.
        
        Args:
            data: Dictionary containing the conversation_id
        """
        conversation_id = data.get('conversation_id')
        if conversation_id:
            from flask_socketio import leave_room
            leave_room(conversation_id)
            emit('status', {'msg': f'Left conversation {conversation_id}'}, room=conversation_id)
    
    @socketio.on('send_message')
    def on_message(data):
        """Handle a new message via WebSocket.
        
        Args:
            data: Dictionary containing conversation_id, sender, content and optional client_message_id
        """
        conversation_id = data.get('conversation_id')
        sender = data.get('sender')
        content = data.get('content')
        client_message_id = data.get('client_message_id')
        
        if not all([conversation_id, sender, content]):
            emit('error', {'msg': 'Missing required fields'})
            return
            
        message = conversation_service.add_message(conversation_id, sender, content)
        if message:
            message_data = message.to_dict()
            if client_message_id:
                message_data['client_message_id'] = client_message_id
                
            emit('new_message', message_data, room=conversation_id)
        else:
            emit('error', {'msg': 'Failed to add message'})
    
    @socketio.on('transcribe')
    def on_transcribe(data):
        """Transcribe audio data via WebSocket.
        
        Args:
            data: Dictionary containing audio_data (Base64 encoded)
        """
        audio_base64 = data.get('audio_data', '')
        conversation_id = data.get('conversation_id')
        sender = data.get('sender', 'client')
        
        if not audio_base64 or not conversation_id:
            emit('error', {'msg': 'Audio data and conversation ID are required'})
            return
            
        try:
            # Decode base64 audio data
            audio_data = base64.b64decode(audio_base64.split(',')[1])
            
            # Transcribe audio
            text = transcription_service.transcribe(audio_data)
            
            if text:
                # Add message to conversation
                message = conversation_service.add_message(conversation_id, sender, text)
                if message:
                    emit('new_message', message.to_dict(), room=conversation_id)
                
                # Send transcription result
                emit('transcription_result', {'text': text, 'sender': sender}, room=conversation_id)
            else:
                emit('error', {'msg': 'Transcription failed'})
        except Exception as e:
            emit('error', {'msg': f'Transcription failed: {str(e)}'})
    
    @socketio.on('clear_conversation')
    def on_clear_conversation(data):
        """Handle clearing a conversation via WebSocket.
        
        Args:
            data: Dictionary containing conversation_id
        """
        conversation_id = data.get('conversation_id')
        
        if not conversation_id:
            emit('error', {'msg': 'Conversation ID is required'})
            return
        
        # Intenta obtener la conversación
        conversation = conversation_service.get_conversation(conversation_id)
        if not conversation:
            emit('error', {'msg': 'Conversation not found'})
            return
            
        # Limpiar los mensajes pero mantener la conversación
        conversation.messages = []
        
        # Guardar la conversación actualizada
        if conversation_service._save_conversation(conversation):
            # Notificar a todos los clientes en la sala que la conversación ha sido limpiada
            emit('conversation_cleared', {'conversation_id': conversation_id}, room=conversation_id)
        else:
            emit('error', {'msg': 'Failed to clear conversation'}) 