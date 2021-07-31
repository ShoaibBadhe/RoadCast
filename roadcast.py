from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create flask instance
app = Flask(__name__)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/postgres'
app.config['SQLALCHEMY_BINDS'] = {'sample': 'mysql://root@localhost/shoaib'}

# secret key
app.config['SECRET_KEY'] = 'my super secret key'

# initialize database
db = SQLAlchemy(app)


# create model for postgresql db
class postgres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # create string
    def __repr__(self):
        return '<Name %r>' % self.name


# create model for mysql db
class sample(db.Model):
    __bind_key__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    added = db.Column(db.DateTime, default=datetime.utcnow)

    # create string
    def __repr__(self):
        return '<Name %r>' % self.name


class UsersForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('submit')


# create a route decorator for postgresql form
@app.route('/', methods=['GET', 'POST'])
def add_user():
    flash('PostgreSQL form')
    name = None
    form = UsersForm()
    if form.validate_on_submit():
        user = postgres.query.filter_by(email=form.email.data).first()
        if user is None:
            user = postgres(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('Added to PostgreSQL Database succesfully')
    our_users = postgres.query.order_by(postgres.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


# create a route to postgresql database
@app.route('/PostgreSQL')
def user1():
    flash('PostgreSQL Database')
    our_users = postgres.query.order_by(postgres.date_added)
    return render_template('db.html', our_users=our_users)


# create a route to mysql database
@app.route('/MySQL')
def user3():
    flash('MySQL Database')
    our_users = sample.query.order_by(sample.added)
    return render_template('db.html', our_users=our_users)


# create a route decorator for mysql form
@app.route('/MySQLform', methods=['GET', 'POST'])
def one_user():
    flash('MySQL Form')
    name = None
    form = UsersForm()
    if form.validate_on_submit():
        user = sample.query.filter_by(email=form.email.data).first()
        if user is None:
            user = sample(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('Added to MySQL Database succesfully')
    our_users = sample.query.order_by(sample.added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


if __name__ == '__main__':
    app.run(debug=True)
