from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from http import HTTPStatus

from src.settings import config
from src.run_api import run_text2sql_api


class Text2SQLServer:
    """Flask server class for Text2SQL API"""

    def __init__(self):
        """Initialize Flask application and configuration"""
        self.app = Flask(__name__)
        CORS(self.app)
        self.config = config

        # Load server configuration
        self.server_config = self.config.get('server', {'host':'0.0.0.0', 'port':5001, 'debug':False})

        # Setup rate limiter
        self.limiter = Limiter(
            get_remote_address,
            app=self.app,
            default_limits=["50 per minute"]  # Limit API usage
        )

        # Register routes and configurations
        self.register_routes()
        self.setup_global_configs()


    def register_routes(self):
        """Register all API routes"""
        self.app.add_url_rule(rule='/', endpoint='home', view_func=self.home)
        self.app.add_url_rule(rule='/run_api', endpoint='text2sql', view_func=self.text2sql_endpoint, methods=['POST'], )
        self.app.add_url_rule(rule='/health', endpoint='health_check', view_func=self.health_check, methods=['GET'])
        self.app.add_url_rule(rule='/about', endpoint='about', view_func=self.about, methods=['GET'])

 

    def setup_global_configs(self):
        """Global configurations for security, cache, and response modifications"""
        
        @self.app.after_request
        def add_headers(response):
            """Modify headers to disable caching and improve security"""
            # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

            # Security headers
            # response.headers["X-Frame-Options"] = "DENY"
            # response.headers["X-Content-Type-Options"] = "nosniff"
            # response.headers["Referrer-Policy"] = "no-referrer"
            # response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"

            return response


    def home(self):
        """Render the index.html template."""
        return render_template("index.html")
    
    # @app.route('/about', methods=['GET'])
    def about(self):
        """Render the about.html template."""
        return render_template("about.html")


    def text2sql_endpoint(self):
        """Endpoint to handle Text2SQL queries and return the result"""
        try:
            data = request.get_json()

            if not data or 'query' not in data:
                return jsonify({'error': 'Missing query parameter'}), HTTPStatus.BAD_REQUEST

            query = data['query']
            result = run_text2sql_api(query)

            return jsonify({'status':'success', 'result':result}), HTTPStatus.OK

        except Exception as e:
            return jsonify({'status':'error', 'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


    def health_check(self):
        """Health check endpoint to verify the server status"""
        return jsonify({'status':'healthy', 'message':'Text2SQL API is running'}), HTTPStatus.OK


    def run(self):
        """Run the Flask server with configuration from config.yml"""
        host = self.server_config.get('host', '0.0.0.0')
        port = self.server_config.get('port', 5001)
        debug = self.server_config.get('debug', False)

        print(f"Starting Text2SQL server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    # Create and run server instance
    server = Text2SQLServer()
    server.run()



