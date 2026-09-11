"""Mod Suite — all-in-one mod dashboard."""
from shared.app import create_app
from mod_suite.auth.routes import auth_bp as suite_auth_bp
from mod_suite.api.routes import api_bp as suite_api_bp
from mod_suite.routes import main_bp as suite_main_bp

def create_app():
    app = create_app()
    app.register_blueprint(suite_main_bp)
    app.register_blueprint(suite_auth_bp)
    app.register_blueprint(suite_api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
