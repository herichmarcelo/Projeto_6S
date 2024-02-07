# auditorias_routes.py
from flask import Blueprint, render_template

# Defina o caminho do template como 'auditorias_templates'
auditorias_bp = Blueprint('auditorias', __name__, template_folder='auditorias_templates')

@auditorias_bp.route('/patio')
def patio():
    return render_template('patio.html')