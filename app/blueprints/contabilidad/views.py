from flask import render_template
from . import contabilidad_bp

@contabilidad_bp.route('/')
def index():
    return render_template('contabilidad/index.html')
