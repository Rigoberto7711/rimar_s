from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import TasaDeCambio
from .forms import TasaDeCambioForm  # Asegúrate de que esto es correcto
from . import tasas_bp  # Importa el blueprint ya definido
from datetime import datetime

@tasas_bp.route('/')
def index():
    ultima_tasa = TasaDeCambio.query.order_by(TasaDeCambio.id.desc()).first()
    return render_template('index.html', ultima_tasa=ultima_tasa)

@tasas_bp.route('/definir_tasas', methods=['GET', 'POST'])
@login_required
def definir_tasas():
    if not current_user.is_authenticated or current_user.role not in ['administrador', 'supervisor']:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('auth.login'))

    form = TasaDeCambioForm()
    if form.validate_on_submit():
        # Convertir la cadena de fecha del formulario a un objeto date
        fecha_str = form.fecha.data  # La cadena de fecha en formato 'DD/MM/YYYY'
        try:
            fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y').date()
        except ValueError:
            flash('Formato de fecha inválido. Usa DD/MM/YYYY.', 'danger')
            return render_template('tasas/definir_tasas.html', form=form)
        
        # Verificar si la fecha ya está registrada en la base de datos
        existing_tasa = TasaDeCambio.query.filter_by(fecha=fecha_obj).first()
        if existing_tasa:
            flash('Esta fecha ya se encuentra registrada para estas tasas de cambio.', 'danger')
            return render_template('tasas/definir_tasas.html', form=form)        
        
        new_tasa = TasaDeCambio(
            fecha=fecha_obj,  # Aquí se usa el objeto fecha_obj
            tasa_oficial=form.tasa_oficial.data,
            tasa_compra=form.tasa_compra.data,
            tasa_venta=form.tasa_venta.data,
            tasa_wu=form.tasa_wu.data
        )
        db.session.add(new_tasa)
        db.session.commit()
        flash('Tasa de cambio definida exitosamente.', 'success')
        return redirect(url_for('index'))
    
    return render_template('tasas/definir_tasas.html', form=form)

@tasas_bp.route('/calcular_cambio', methods=['GET', 'POST'])
def calcular_cambio():
    if request.method == 'POST':
        tipo_cambio = request.form.get('tipo_cambio')
        monto = float(request.form.get('monto'))

        # Obtener el último registro de TasaDeCambio
        ultima_tasa = TasaDeCambio.query.order_by(TasaDeCambio.id.desc()).first()

        if tipo_cambio == 'venta':
            tasa = ultima_tasa.tasa_venta
        elif tipo_cambio == 'compra':
            tasa = ultima_tasa.tasa_compra

        # Calcular el cambio
        cambio = monto * tasa

        return render_template('tasas/resultado_cambio.html', cambio=cambio, monto=monto, tipo_cambio=tipo_cambio)

    return render_template('tasas/calcular_cambio.html')

@tasas_bp.route('/resultado_cambio')
def resultado_cambio():
    tipo_cambio = request.args.get('tipo_cambio')
    monto = request.args.get('monto')
    cambio = request.args.get('cambio')
    return render_template('tasas/resultado_cambio.html', tipo_cambio=tipo_cambio, monto=monto, cambio=cambio)