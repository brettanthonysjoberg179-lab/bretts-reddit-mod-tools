"""Mod Log — moderation log viewer and analytics."""
from shared.app import create_app
from mod_log.auth.routes import auth_bp as log_auth_bp
from mod_log.api.routes import api_bp as log_api_bp
from mod_log.routes import main_bp as log_main_bp

def create_app():
    app = create_app()
    app.register_blueprint(log_main_bp)
    app.register_blueprint(log_auth_bp)
    app.register_blueprint(log_api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5003, debug=True)
