from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.models.usuario import Usuario, buscar_por_email

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        usuario_dict = buscar_por_email(email)
        if usuario_dict:
            u = Usuario(
                usuario_dict['nome'],
                usuario_dict['email'],
                usuario_dict['senha_hash'],
                usuario_dict['tipo'],
            )
            if u.verificar_senha(senha):
                session['usuario_id'] = email
                session['nome'] = usuario_dict['nome']
                session['tipo'] = usuario_dict['tipo']
                return redirect(url_for('dashboard.dashboard'))

        flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('login.login'))
