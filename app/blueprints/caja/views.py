from flask import Blueprint, render_template, request

caja_bp = Blueprint('caja', __name__)

@caja_bp.route('/calcular_cambio', methods=['GET', 'POST'])
def calcular_cambio():
    if request.method == 'POST':
        tipo_cambio = request.form.get('tipo_cambio')
        monto = float(request.form.get('monto'))

        # Obtener el último registro de TasaDeCambio
        ultima_tasa = TasaDeCambio.query.order_by(TasaDeCambio.id.desc()).first()

        if tipo_cambio == 'venta':
            tasa = ultima_tasa.tasa_venta
        elif tipo_cambio == 'compra':  # compra
            tasa = ultima_tasa.tasa_compra

        # Calcular el cambio
        cambio = monto * tasa

        return render_template('resultado_cambio.html', cambio=cambio, monto=monto, tipo_cambio=tipo_cambio)

    return render_template('caja/calcular_cambio.html')