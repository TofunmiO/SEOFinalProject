from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
import requests


app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '25d5ad000a6a0c19ef1dc9c409582f31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

""" If we incorporate accounts
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
"""

@app.route("/")
def home():
    return render_template('home.html',
                           subtitle='Welcome to AfriXplore!',
                           text="See the beauty of Africa")


@app.route("/discover")
def discover():
    return render_template('discover.html',
                           subtitle='Discover',
                           text='Discover the beauty of Africa!')


@app.route("/travel")
def travel():
    return render_template('travel.html',
                           subtitle='Travel',
                           flight='Find your next flight:',
                           hotel='Find your next accommodation:')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")