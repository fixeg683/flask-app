import json
import os
from openai import OpenAI
from flask import current_app

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

class CustomerSupportChatbot:
    def __init__(self):
        self.system_prompt = """You are a helpful customer support assistant for Digital Store, 
        an e-commerce platform that sells digital products including movies, software, and games.
        
        Your role is to:
        - Help customers with questions about products, orders, and account issues
        - Provide information about pricing, availability, and product features
        - Assist with technical support for digital downloads
        - Guide users through the purchase process
        - Handle refund and return inquiries professionally
        
        Key information about Digital Store:
        - We sell digital movies, software, and games
        - All products are delivered digitally after purchase
        - We accept PayPal payments
        - Users can create accounts to track their purchases
        - Products include popular movies, productivity software, and entertainment games
        
        Always be helpful, professional, and concise in your responses.
        If you cannot answer a specific question, politely direct the customer to contact human support.
        """
    
    def get_response(self, user_message, conversation_history=None):
        """Get a response from the chatbot for customer support"""
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "error": None
            }
            
        except Exception as e:
            current_app.logger.error(f"Chatbot error: {str(e)}")
            return {
                "success": False,
                "response": "I'm sorry, I'm having trouble connecting right now. Please try again later or contact our support team.",
                "error": str(e)
            }
    
    def analyze_sentiment(self, message):
        """Analyze customer message sentiment for support prioritization"""
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a sentiment analysis expert. Analyze the sentiment of customer support messages and provide a rating from 1 to 5 stars (1=very negative, 5=very positive) and a confidence score between 0 and 1. Also determine if this is urgent (true/false). Respond with JSON in this format: {'rating': number, 'confidence': number, 'urgent': boolean, 'emotion': 'string'}"
                    },
                    {"role": "user", "content": message}
                ],
                response_format={"type": "json_object"},
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                "rating": max(1, min(5, round(result.get("rating", 3)))),
                "confidence": max(0, min(1, result.get("confidence", 0.5))),
                "urgent": result.get("urgent", False),
                "emotion": result.get("emotion", "neutral")
            }
            
        except Exception as e:
            current_app.logger.error(f"Sentiment analysis error: {str(e)}")
            return {
                "rating": 3,
                "confidence": 0.5,
                "urgent": False,
                "emotion": "neutral"
            }

# Global chatbot instance
chatbot = CustomerSupportChatbot()