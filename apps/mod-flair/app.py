"""Mod Flair — manage and assign flair."""
from shared.app import create_app
from mod_flair.auth.routes import auth_bp as flair_auth_bp
from mod_flair.api.routes import api_bp as flair_api_bp
from mod_flair.routes import main_bp as flair_main_bp

def create_app():
    app = create_app()
    app.register_blueprint(flair_main_bp)
    app.register_blueprint(flair_auth_bp)
    app.register_blueprint(flair_api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5005, debug=True)
