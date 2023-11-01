# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
import os

db_user = os.environ.get('MYSQL_USER', 'default_user')
db_password = os.environ.get('MYSQL_ROOT_PASSWORD', 'default_password')
db_name = os.environ.get('MYSQL_DATABASE', 'default_database')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_password}@database/{db_name}'
app.secret_key = 'your_secret_key'  # Clé secrète pour les messages flash

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #birthdate = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=True)
# Gestionnaire de contexte d'application pour la création de la base de données
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        birthdate = request.form['birthdate']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('L\'utilisateur existe déjà.', 'error')
        else:
            user = User(first_name=first_name, last_name=last_name, email=email, birthdate=birthdate)
            with app.app_context():
                db.session.add(user)
                db.session.commit()
            flash('L\'utilisateur a été ajouté avec succès.', 'success')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

