"""Mod Mail — read and respond to mod mail."""
from shared.app import create_app
from mod_mail.auth.routes import auth_bp as mail_auth_bp
from mod_mail.api.routes import api_bp as mail_api_bp
from mod_mail.routes import main_bp as mail_main_bp

def create_app():
    app = create_app()
    app.register_blueprint(mail_main_bp)
    app.register_blueprint(mail_auth_bp)
    app.register_blueprint(mail_api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5004, debug=True)
