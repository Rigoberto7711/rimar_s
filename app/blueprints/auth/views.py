from flask import render_template, redirect, url_for, flash, request
from . import auth_bp
from app import db
from app.models import Agency, User, Permission
from app.forms import LoginForm # Asegúrate de que AgencyForm esté importado Importa UserForm aquí
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import AgencyForm, UserForm, PermissionForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm, RegistrationForm

@auth_bp.route('/create_agency', methods=['GET', 'POST'])
@login_required
def create_agency():
    form = AgencyForm()
    if form.validate_on_submit():
        # Verificar si ya existe una agencia con el mismo nombre
        existing_agency = Agency.query.filter_by(name=form.name.data).first()
        if existing_agency:
            flash('El nombre de la agencia ya existe. Por favor, elige otro nombre.', 'danger')
        else:
            new_agency = Agency(name=form.name.data)
            db.session.add(new_agency)
            db.session.commit()
            flash('Agencia creada exitosamente.', 'success')
            return redirect(url_for('index'))
    return render_template('auth/create_agency.html', form=form)

@auth_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('El nombre de usuario ya existe. Por favor, elige otro nombre.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, password=hashed_password, agency_id=form.agency_id.data, role=form.role.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('index'))
    return render_template('auth/create_user.html', form=form)


@auth_bp.route('/create_permission', methods=['GET', 'POST'])
def create_permission():
    form = PermissionForm()
    if form.validate_on_submit():
        permission = Permission(name=form.name.data, description=form.description.data)
        db.session.add(permission)
        db.session.commit()
        flash('Permiso creado exitosamente!', 'success')
        return redirect(url_for('auth.create_permission'))
    return render_template('auth/create_permission.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password, agency_id=form.agency_id.data, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)