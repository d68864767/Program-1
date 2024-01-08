from flask import Flask, request, jsonify, render_template
from src.content_management.content_generator import ContentGenerator
from src.utils.logger import Logger
from src.utils.utils import load_json_config

# Initialize Flask application
app = Flask(__name__, template_folder='../ui')

# Initialize Logger
logger = Logger().get_logger()

# Load project settings
project_settings = load_json_config('config/project_settings.json')
web_service_settings = project_settings.get('web_service_settings', {})

# Initialize ContentGenerator
content_generator = ContentGenerator()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('main_page.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    """
    Endpoint to generate content based on the input provided.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

        # Extract required fields from data
        prompt = data.get('prompt')
        if not prompt:
            raise ValueError("Prompt is required to generate content")

        # Generate content using the ContentGenerator
        generated_content = content_generator.generate(prompt)

        # Return generated content as JSON
        return jsonify({'content': generated_content}), 200

    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run Flask app
    app.run(
        host=web_service_settings.get('host', '127.0.0.1'),
        port=web_service_settings.get('port', 5000),
        debug=web_service_settings.get('debug', True)
    )
