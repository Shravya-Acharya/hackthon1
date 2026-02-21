from flask import Blueprint, request, jsonify
from utils.chatbot_utils import get_chatbot_response

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data.get('message', '')
    response = get_chatbot_response(message)
    return jsonify({'response': response})