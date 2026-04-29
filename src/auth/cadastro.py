import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.usuario import Usuario, carregar_usuarios, salvar_usuarios, buscar_por_email

cadastro_bp = Blueprint('cadastro', __name__)


def _email_valido(email):
    return re.match(r'^[\w.+-]+@[\w-]+\.[a-z]{2,}$', email, re.IGNORECASE)


def _senha_valida(senha):
    return len(senha) >= 8


@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        tipo = request.form.get('tipo', 'aluno')

        if not nome:
            flash('Nome é obrigatório.', 'danger')
        elif not _email_valido(email):
            flash('E-mail inválido.', 'danger')
        elif not _senha_valida(senha):
            flash('Senha deve ter pelo menos 8 caracteres.', 'danger')
        elif buscar_por_email(email):
            flash('E-mail já cadastrado.', 'danger')
        else:
            usuario = Usuario(nome, email, '', tipo)
            usuario.set_senha(senha)
            usuarios = carregar_usuarios()
            usuarios.append(usuario.to_dict())
            salvar_usuarios(usuarios)
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('login.login'))

    return render_template('cadastro.html')
