from flask import render_template
from . import clientes_bp

@clientes_bp.route('/')
def index():
    return render_template('clientes/index.html')
