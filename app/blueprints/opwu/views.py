from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models import OpWu, TasaDeCambio
from . import opwu_bp  # Importa el Blueprint

@opwu_bp.route('/operaciones_wu', methods=['GET', 'POST'])
@login_required
def operaciones_wu():
    ultima_tasa = TasaDeCambio.query.order_by(TasaDeCambio.id.desc()).first()
    if request.method == 'POST':
        # Verifica todos los datos enviados desde el formulario
        print(request.form)
        
        # Validar campos vacíos y numéricos
        montotrus = request.form.get('montotrus')
        montopus = request.form.get('montopus')
        montotrcs = request.form.get('montotrcs')
        montopcs = request.form.get('montopcs')
        ajuste_CS = request.form.get('ajuste_CS')

        if not montotrus or not montopus or not montotrcs or not montopcs:
            flash('Todos los campos de monto deben ser completados.')
            return redirect(url_for('opwu.operaciones_wu'))

        try:
            montotrus = float(montotrus)
            montopus = float(montopus)
            montotrcs = float(montotrcs)
            montopcs = float(montopcs)
        except ValueError:
            flash('Todos los campos de monto deben ser valores numéricos.')
            return redirect(url_for('opwu.operaciones_wu'))

        # Validar ajuste_CS
        try:
            ajuste_CS = float(ajuste_CS)
            if ajuste_CS > 5 or ajuste_CS < -5:
                flash('El valor del ajuste no debe ser mayor ni menor que 5, favor revisar detalle de moneda.')
                return redirect(url_for('opwu.operaciones_wu'))
        except ValueError:
            flash('El valor del ajuste debe ser un número válido.')
            return redirect(url_for('opwu.operaciones_wu'))

        # Procesar los datos del formulario
        try:
            new_operation = OpWu(
                transaccion=request.form['transaccion'],
                tipo_operacion=request.form['tipo_operacion'],
                montotrus=montotrus,
                montopus=montopus,
                montotrcs=montotrcs,
                montopcs=montopcs,
                montoi_1000_CS=float(request.form.get('montoi_1000_CS', 0)),
                montoi_500_CS=float(request.form.get('montoi_500_CS', 0)),
                montoi_200_CS=float(request.form.get('montoi_200_CS', 0)),
                montoi_100_CS=float(request.form.get('montoi_100_CS', 0)),
                montoi_50_CS=float(request.form.get('montoi_50_CS', 0)),
                montoi_20_CS=float(request.form.get('montoi_20_CS', 0)),
                montoi_10_CS=float(request.form.get('montoi_10_CS', 0)),
                montoi_5_CS=float(request.form.get('montoi_5_CS', 0)),
                montoi_1_CS=float(request.form.get('montoi_1_CS', 0)),
                total_entradas_CS=float(request.form.get('total_entradas_CS', 0) or 0),
                cambioi_CS=float(request.form.get('cambioi_CS', 0) or 0),
                montos_1000_CS=float(request.form.get('montos_1000_CS', 0)),
                montos_500_CS=float(request.form.get('montos_500_CS', 0)),
                montos_200_CS=float(request.form.get('montos_200_CS', 0)),
                montos_100_CS=float(request.form.get('montos_100_CS', 0)),
                montos_50_CS=float(request.form.get('montos_50_CS', 0)),
                montos_20_CS=float(request.form.get('montos_20_CS', 0)),
                montos_10_CS=float(request.form.get('montos_10_CS', 0)),
                montos_5_CS=float(request.form.get('montos_5_CS', 0)),
                montos_1_CS=float(request.form.get('montos_1_CS', 0)),
                total_Salidas_CS=float(request.form.get('total_Salidas_CS', 0) or 0),
                ajuste_CS=ajuste_CS,
                montoE_100_US=float(request.form.get('montoE_100_US', 0)),
                montoE_50_US=float(request.form.get('montoE_50_US', 0)),
                montoE_20_US=float(request.form.get('montoE_20_US', 0)),
                montoE_10_US=float(request.form.get('montoE_10_US', 0)),
                montoE_5_US=float(request.form.get('montoE_5_US', 0)),
                montoE_1_US=float(request.form.get('montoE_1_US', 0)),
                total_entradas_US=float(request.form.get('total_entradas_US', 0) or 0),
                cambioE_US=float(request.form.get('cambioE_US', 0) or 0),
                montoP_100_US=float(request.form.get('montoP_100_US', 0)),
                montoP_50_US=float(request.form.get('montoP_50_US', 0)),
                montoP_20_US=float(request.form.get('montoP_20_US', 0)),
                montoP_10_US=float(request.form.get('montoP_10_US', 0)),
                montoP_5_US=float(request.form.get('montoP_5_US', 0)),
                montoP_1_US=float(request.form.get('montoP_1_US', 0)),
                total_salidas_US=float(request.form.get('total_salidas_US', 0) or 0),
                ajuste_US=float(request.form.get('ajuste_US', 0) or 0),
                ajuste=float(request.form.get('ajuste', 0) or 0)
            )

            # Intentar guardar la operación con reintentos
            retries = 5
            for _ in range(retries):
                try:
                    db.session.add(new_operation)
                    db.session.commit()
                    flash('Operación guardada exitosamente!', 'success')
                    break
                except OperationalError as e:
                    db.session.rollback()
                    if "database is locked" in str(e):
                        time.sleep(1)  # Esperar 1 segundo antes de reintentar
                    else:
                        flash(f'Error al guardar la operación: {str(e)}', 'error')
                        break
            else:
                flash('Error al guardar la operación: la base de datos está bloqueada.', 'error')

        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar la operación: {str(e)}', 'error')
        
        # Redirigir a la misma página para mostrar resultados o errores
        return redirect(url_for('opwu.operaciones_wu'))
    else:
        # Asumiendo que hay un template que renderizar cuando GET
        return render_template('opwu/operaciones_wu.html', ultima_tasa=ultima_tasa)

