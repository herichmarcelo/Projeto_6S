# auditorias_routes.py
from flask import Blueprint, render_template

# Defina o caminho do template como 'auditorias_templates'
auditorias_bp = Blueprint('auditorias', __name__, template_folder='auditorias_templates')

@auditorias_bp.route('/patio')
def patio():
    return render_template('patio.html')

@auditorias_bp.route('/adm')
def adm():
    return render_template('adm.html')

@auditorias_bp.route('/externas')
def externas():
    return render_template('externas.html')

@auditorias_bp.route('/producao')
def producao():
    return render_template('producao.html')