from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields import DateField
from app.models import Agency


class AgencyForm(FlaskForm):
    name = StringField('Nombre de la Agencia', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Crear Agencia')

class UserForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    agency_id = SelectField('Agencia', coerce=int, choices=[], validators=[DataRequired()])
    role = SelectField('Rol', choices=[('administrador', 'Administrador'), ('supervisor', 'Supervisor'), ('usuario', 'Usuario')], validators=[DataRequired()])
    submit = SubmitField('Crear Usuario')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.agency_id.choices = [(agency.id, agency.name) for agency in Agency.query.all()]

class PermissionForm(FlaskForm):
    name = StringField('Nombre del Permiso', validators=[DataRequired(), Length(min=2, max=50)])
    description = StringField('Descripción', validators=[Length(max=200)])
    submit = SubmitField('Crear Permiso')
    
class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    agency_id = SelectField('Agencia', choices=[], coerce=int, validators=[DataRequired()])  # Rellenar opciones en la vista
    role = SelectField('Rol', choices=[('administrador', 'Administrador'), ('supervisor', 'Supervisor'), ('usuario', 'Usuario')], validators=[DataRequired()])
    submit = SubmitField('Registrar')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.agency_id.choices = [(agency.id, agency.name) for agency in Agency.query.all()]


class TasaDeCambioForm(FlaskForm):
    fecha = StringField('Fecha', validators=[DataRequired()])
    tasa_oficial = FloatField('Tasa Oficial', validators=[DataRequired()])
    tasa_compra = FloatField('Tasa de Compra', validators=[DataRequired()])
    tasa_venta = FloatField('Tasa de Venta', validators=[DataRequired()])
    tasa_wu = FloatField('Tasa WU', validators=[DataRequired()])
    tasac_bancos = FloatField('Tasa de Compra Bancos', validators=[DataRequired()])    
    tasav_bancos = FloatField('Tasa de Venta Bancos', validators=[DataRequired()])  
    tasap_banpro = FloatField('Tasa de Preferencial Banpro', validators=[DataRequired()])  
    tasap_lafise = FloatField('Tasa de Compra Bancos', validators=[DataRequired()])      
    submit = SubmitField('Guardar')

