from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, flash

dashboard_bp = Blueprint('dashboard', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faça login primeiro.', 'warning')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome=session.get('nome'), tipo=session.get('tipo'))
