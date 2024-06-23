# app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from . import db

class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    users = db.relationship('User', backref='agency', lazy=True)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    permissions = db.relationship('Permission', secondary='user_permissions', backref='users', lazy='dynamic')

    def __init__(self, username, password, role, agency_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.agency_id = agency_id

    def __repr__(self):
        return f'<User {self.username}>'

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)

user_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class TasaDeCambio(db.Model):
    __tablename__ = 'tasa_de_cambio'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    tasa_oficial = db.Column(db.Float, nullable=False)
    tasa_compra = db.Column(db.Float, nullable=False)
    tasa_venta = db.Column(db.Float, nullable=False)
    tasa_wu = db.Column(db.Float, nullable=False)
    tasac_bancos = db.Column(db.Float, nullable=False)
    tasav_bancos = db.Column(db.Float, nullable=False)
    tasap_banpro = db.Column(db.Float, nullable=False)
    tasap_lafise = db.Column(db.Float, nullable=False)

class OpWu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaccion = db.Column(db.String(50), nullable=False)
    tipo_operacion = db.Column(db.String(50), nullable=False)
    montotrus = db.Column(db.Float, nullable=False)
    montopus = db.Column(db.Float, nullable=False)
    montotrcs = db.Column(db.Float, nullable=False)
    montopcs = db.Column(db.Float, nullable=False)
    montoi_1000_CS = db.Column(db.Float, nullable=False)
    montoi_500_CS = db.Column(db.Float, nullable=False)
    montoi_200_CS = db.Column(db.Float, nullable=False)
    montoi_100_CS = db.Column(db.Float, nullable=False)
    montoi_50_CS = db.Column(db.Float, nullable=False)
    montoi_20_CS = db.Column(db.Float, nullable=False)
    montoi_10_CS = db.Column(db.Float, nullable=False)
    montoi_5_CS = db.Column(db.Float, nullable=False)
    montoi_1_CS = db.Column(db.Float, nullable=False)
    total_entradas_CS = db.Column(db.Float, nullable=False)
    cambioi_CS = db.Column(db.Float, nullable=False)
    montos_1000_CS = db.Column(db.Float, nullable=False)
    montos_500_CS = db.Column(db.Float, nullable=False)
    montos_200_CS = db.Column(db.Float, nullable=False)
    montos_100_CS = db.Column(db.Float, nullable=False)
    montos_50_CS = db.Column(db.Float, nullable=False)
    montos_20_CS = db.Column(db.Float, nullable=False)
    montos_10_CS = db.Column(db.Float, nullable=False)
    montos_5_CS = db.Column(db.Float, nullable=False)
    montos_1_CS = db.Column(db.Float, nullable=False)
    total_Salidas_CS = db.Column(db.Float, nullable=False)
    ajuste_CS = db.Column(db.Float, nullable=False)
    montoE_100_US = db.Column(db.Float, nullable=False)
    montoE_50_US = db.Column(db.Float, nullable=False)
    montoE_20_US = db.Column(db.Float, nullable=False)
    montoE_10_US = db.Column(db.Float, nullable=False)
    montoE_5_US = db.Column(db.Float, nullable=False)
    montoE_1_US = db.Column(db.Float, nullable=False)
    total_entradas_US = db.Column(db.Float, nullable=False)
    cambioE_US = db.Column(db.Float, nullable=False)
    montoP_100_US = db.Column(db.Float, nullable=False)
    montoP_50_US = db.Column(db.Float, nullable=False)
    montoP_20_US = db.Column(db.Float, nullable=False)
    montoP_10_US = db.Column(db.Float, nullable=False)
    montoP_5_US = db.Column(db.Float, nullable=False)
    montoP_1_US = db.Column(db.Float, nullable=False)
    total_salidas_US = db.Column(db.Float, nullable=False)
    ajuste_US = db.Column(db.Float, nullable=False)
    ajuste = db.Column(db.Float, nullable=False)

# app/blueprints/tasas/views.py

from flask import Blueprint, render_template, request, redirect, url_for
from app.models import TasaDeCambio
from .forms import TasaDeCambioForm

# Resto de las definiciones para las vistas
