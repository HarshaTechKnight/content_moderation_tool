from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from moderation import ContentModerator
from utils.helpers import format_moderation_result
from utils.logger import setup_logger
from config import Config

app = Flask(__name__)
api = Api(app)
logger = setup_logger(__name__)

# Initialize moderator
moderator = ContentModerator()

class ModerationResource(Resource):
    def post(self):
        """Moderate content from POST request."""
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return {"error": "Missing 'text' in request body"}, 400
                
            text = data['text']
            logger.info(f"Moderating text: {text[:50]}...")  # Log first 50 chars
            
            # Moderate the content
            result = moderator.moderate(text)
            
            # Format the response
            response = {
                "text": text,
                "moderation_result": format_moderation_result(result)
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error during moderation: {str(e)}")
            return {"error": "Internal server error"}, 500

class HealthCheckResource(Resource):
    def get(self):
        """Health check endpoint."""
        return {"status": "healthy", "version": "1.0.0"}

# Add resources to API
api.add_resource(ModerationResource, '/api/moderate')
api.add_resource(HealthCheckResource, '/api/health')

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)