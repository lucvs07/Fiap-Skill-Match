from flask import Flask, redirect, url_for, session
from src.auth.cadastro import cadastro_bp
from src.auth.login import login_bp
from src.views.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'skill-match-secret-key-fiap-2025'

    app.register_blueprint(cadastro_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def index():
        if 'usuario_id' in session:
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('login.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
