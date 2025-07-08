from flask import Blueprint, request, jsonify, render_template, session
from chatbot import chatbot
import json

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@chatbot_bp.route('/')
def chatbot_page():
    """Render the chatbot interface page"""
    return render_template('chatbot.html')

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Get conversation history from session
        conversation_history = session.get('chat_history', [])
        
        # Get response from chatbot
        result = chatbot.get_response(user_message, conversation_history)
        
        if result['success']:
            # Update conversation history
            conversation_history.append({"role": "user", "content": user_message})
            conversation_history.append({"role": "assistant", "content": result['response']})
            
            # Keep only last 10 messages to avoid session bloat
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
            
            session['chat_history'] = conversation_history
            
            # Analyze sentiment for support prioritization
            sentiment = chatbot.analyze_sentiment(user_message)
            
            return jsonify({
                'success': True,
                'response': result['response'],
                'sentiment': sentiment
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'response': result['response']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'response': 'Sorry, I encountered an error. Please try again.'
        }), 500

@chatbot_bp.route('/clear', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    session.pop('chat_history', None)
    return jsonify({'success': True, 'message': 'Chat history cleared'})

@chatbot_bp.route('/history')
def chat_history():
    """Get current chat history"""
    history = session.get('chat_history', [])
    return jsonify({'history': history})