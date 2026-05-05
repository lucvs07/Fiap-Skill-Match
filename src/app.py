from flask import Flask, redirect, url_for, session
from src.auth.cadastro import cadastro_bp
from src.auth.login import login_bp
from src.views.dashboard import dashboard_bp
from src.views.projetos import projetos_bp
from src.views.mentores import mentores_bp
from src.views.perfil import perfil_bp
from src.views.alunos import alunos_bp
from src.models.convite import carregar_convites


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'skill-match-secret-key-fiap-2025'

    app.register_blueprint(cadastro_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(projetos_bp)
    app.register_blueprint(mentores_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(alunos_bp)

    @app.context_processor
    def inject_convites_pendentes():
        nome = session.get('nome')
        tipo = session.get('tipo')
        if nome and tipo in ('aluno', 'mentor'):
            pendentes = sum(
                1 for c in carregar_convites()
                if c['destinatario'] == nome and c['status'] == 'pendente'
            )
        else:
            pendentes = 0
        return {'convites_pendentes': pendentes}

    @app.route('/')
    def index():
        if 'usuario_id' in session:
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('login.login'))

    return app


