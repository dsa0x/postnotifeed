
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField, SubmitField
from flask_wtf import FlaskForm
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import helpers
import igscraper
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mail import Message, Mail
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#'postgresql://{}:{}@{}/{}'.format(app.config['POSTGRES_USER'],app.config['POSTGRES_PASSWORD'],app.config['POSTGRES_URL'],app.config['POSTGRES_DB'])
#'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app,db)
mail = Mail(app)
#manager = Manager(app)


#manager.add_command('db', MigrateCommand)

###################################################################
######      MODELS    ############
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer())
    username = db.Column(db.String())
    number_of_posts = db.Column(db.Integer())
    service_type = db.Column(db.String())
    last_post = db.Column(db.String())

    def __init__(self, quantity, username, service_type, number_of_posts):
        self.quantity = quantity
        self.username = username
        self.service_type = service_type
        self.number_of_posts = number_of_posts

################################################################
################################################################
######      FORMS    ############
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    service_type = StringField('Service type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    number_of_posts = IntegerField(
        'Number of Posts', validators=[DataRequired()])
    submit = SubmitField('Submit')

################################################################
################################################################
######      MAILER    ############

def email_sender(subject, template, **kwargs):
    msg = Message(
        subject=subject, sender=app.config['SENDER'], recipients=[app.config['RECIPIENT']])
    msg.body = render_template(template,**kwargs)
    mail.send(msg)


################################################################
################################################################
######      ROUTES    ############
@app.route('/',methods=['GET','POST'])
def index():
    form = UserForm(request.form)
    subject = 'New auto order'
    template = 'adduser.txt'
    if form.validate_on_submit():
        print(request.method)
        user = User(quantity=form.quantity.data, username=form.username.data,
        service_type=form.service_type.data,number_of_posts=form.number_of_posts.data)
        user.last_post = igscraper.linkget(user.username)['link']
        #user.last_post = helpers.getposts(user.username, user.service_type)['shorty']
        db.session.add(user)
        db.session.commit()
        email_sender(subject, template, user=user)
        flash('User has been added')
    return render_template('index.html',form=form)

#@sched.scheduled_job('interval', minutes=1)
@app.route('/users')
def users():
    users = User.query.all()
    subject = 'New Post Link'
    template = 'email.txt'
    i = 0
    for user in users:
        #number_of_posts = user.number_of_posts
        i += 1
        #postlink = helpers.getposts(user.username,user.service_type)['shorty']
        postlink = igscraper.linkget(user.username)['link']
        if postlink != user.last_post and user.number_of_posts > 0:
            user.number_of_posts -=1
            user.last_post = postlink
            db.session.commit()
            email_sender(subject,template,user=user)
        elif user.number_of_posts <= 0:
            template = 'finished.txt'
            subject = user.username.title() + ' Post Exhausted'
            email_sender(subject, template, user=user)
            db.session.delete(user)
            db.session.commit()
    return render_template('users.html', users=users, i=i)


@app.route('/delete/<userr>',methods=['GET', 'POST'])
def delete(userr):
    userr = User.query.filter_by(username=userr).first_or_404()
    db.session.delete(userr)
    db.session.commit()
    return render_template('users.html',userr=userr)


if __name__ == '__main__':
    app.run()