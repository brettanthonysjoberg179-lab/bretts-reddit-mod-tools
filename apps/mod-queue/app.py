"""Mod Queue — queue viewer and bulk processor."""
from shared.app import create_app
from mod_queue.auth.routes import auth_bp as queue_auth_bp
from mod_queue.api.routes import api_bp as queue_api_bp
from mod_queue.routes import main_bp as queue_main_bp

def create_app():
    app = create_app()
    app.register_blueprint(queue_main_bp)
    app.register_blueprint(queue_auth_bp)
    app.register_blueprint(queue_api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5002, debug=True)
