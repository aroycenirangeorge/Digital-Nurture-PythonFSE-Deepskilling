from flask import Flask, jsonify
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)
    
    # Step 45: Global JSON error overrides for 404 and 500 actions
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'status': 'error',
            'data': {'message': 'The requested resource could not be found on this server.'}
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'data': {'message': 'An unexpected internal server error occurred.'}
        }), 500
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()