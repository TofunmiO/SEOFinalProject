from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask_bcrypt import Bcrypt
from sqlalchemy import exc, text
import requests
from api_calls import mediawikiAPI, unsplashAPI, africanCountry
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm, RegistrationForm
import pandas as pd
from map import createMap

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '25d5ad000a6a0c19ef1dc9c409582f31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_table():
    query = text("""CREATE TABLE IF NOT EXISTS ' {} ' (
    country STRING )""".format(str(current_user.get_id())))
    db.engine.execute(query)

class User(db.Model):
    """An admin user capable of viewing reports.
    :param str email: email address of user
    :param str password: encrypted password for the user
    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return f"User('{self.email}')"

@app.route("/")
def home():
    return render_template('home.html',
                           subtitle='Welcome to AfriXplore!',
                           text="Discover the beauty of Africa")


@app.route("/discover", methods=['GET', 'POST'])
def discover():
    if request.method != 'POST':
        country = africanCountry()
        createMap(country)
        session['data'] = [str(country)]
    if request.method == 'POST':
        create_table()
        df = pd.DataFrame(session['data'], columns = ['Country'])
        df.to_sql(current_user.get_id(),
                  con=db.engine,
                  if_exists='append',
                  index=False)
        print(df)
        flash(f'Country added!', 'success')
        return redirect(url_for("countries"))
    return render_template('discover.html',
                           subtitle='Discover',
                           text='Discover the beauty of Africa!',
                           countries = country,
                           textinfo=mediawikiAPI(country),
                           links=unsplashAPI(country))


@app.route("/travel", methods=['GET', 'POST'])
def travel():
    return render_template('travel.html',
                           subtitle='Travel',
                           flight='Find your next flight:',
                           hotel='Find your next accommodation:')


@app.route("/countries")
@login_required
def countries():
    try:
        countries_saved = pd.read_sql_table(current_user.get_id(),
                                      con=db.engine)
        print(countries_saved)
    except ValueError:
        flash(f'No countries found!', 'success')
        return redirect(url_for('home'))
    else:
        countries = []
        textinfo = []
        for row in countries_saved['Country']:
            countries.append(row)
            textinfo.append(mediawikiAPI(row))
    return render_template('countries.html',
                           subtitle='Countries',
                           text='Saved Items',
                           countries=countries,
                           textinfo=textinfo)

# @app.route("/countries", methods=['GET', 'POST'])
# @login_required
# def countries():
#     try:
#         countries_saved = pd.read_sql_table(current_user.get_id(),
#                                       con=db.engine)
#     except ValueError:
#         flash(f'No countries found!', 'success')
#         return redirect(url_for('home'))
#     else:
#         countries = []
#         for row in countries_saved['Country']:
#             countries.append(row)
#         for names in countries:
#             textinfo = mediawikiAPI(names)
#             links = unsplashAPI(names)
#     return render_template('countries.html',
#                            subtitle='Countries',
#                            text='Saved Items',
#                            countries=countries,
#                            textinfo=textinfo,
#                            links=links)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     """For GET requests, display the login form.
#     For POSTS, login the current user by processing the form.
#     """
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.get(form.email.data)
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 user.authenticated = True
#                 db.session.add(user)
#                 db.sessionecommit()
#                 login_user(user, remember=True)
#                 return redirect(url_for("home"))
#     return render_template("login.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                login_user(user, remember=True)
                return redirect(url_for("home"))
        if not user:
            flash(f'Incorrect username or email account for {form.email.data}! Try again!', 'failed')
            return redirect(url_for("login"))
        password = User.query.get(form.password.data)
        if not password:
            flash(f'Incorrect password for {form.email.data}! Try again!', 'failed')
            return redirect(url_for("login"))
        flash(f'Successful login for {form.email.data}!', 'success')
        return redirect(url_for("home")) # if so - send to home page
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash(f'Logged out!', 'success')
    return redirect(url_for("home"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = (bcrypt.generate_password_hash(form.password.data)
                    .decode('utf-8'))
        user = User(email=form.email.data,
                    password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash(f'Username or email account already exists!', 'success')
        else:
            flash(f'Account created for {form.email.data}!', 'success')
            return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True ,host="0.0.0.0")