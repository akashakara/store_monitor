from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/Xampp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    timezone = db.Column(db.String(50), nullable=False)


class BusinessHour(db.Model):
    __tablename__ = 'business_hours'

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time_local = db.Column(db.Time, nullable=False)
    end_time_local = db.Column(db.Time, nullable=False)


class StoreStatus(db.Model):
    __tablename__ = 'store_statuses'

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    timestamp_utc = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    
 
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')



import csv
from datetime import datetime
from pytz import timezone
from .models import Store, BusinessHour, StoreStatus, db


def populate_database():
    with open('stores.csv') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            store_id, timezone_str = row
            store = Store

