# app/blueprints/tasas/forms.py

from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, SubmitField
from wtforms.validators import DataRequired

class TasaDeCambioForm(FlaskForm):
    fecha = DateField('Fecha', validators=[DataRequired()])
    tasa_oficial = FloatField('Tasa Oficial', validators=[DataRequired()])
    tasa_compra = FloatField('Tasa de Compra', validators=[DataRequired()])
    tasa_venta = FloatField('Tasa de Venta', validators=[DataRequired()])
    tasa_wu = FloatField('Tasa WU', validators=[DataRequired()])
    tasac_bancos = FloatField('Tasa C. Bancos', validators=[DataRequired()])
    tasav_bancos = FloatField('Tasa V. Bancos', validators=[DataRequired()])
    tasap_banpro = FloatField('Tasa P. Banpro', validators=[DataRequired()])
    tasap_lafise = FloatField('Tasa P. Lafise', validators=[DataRequired()])
    submit = SubmitField('Guardar')
