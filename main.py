from flask import Flask, render_template, flash, session, url_for, redirect
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Project(db.Model):
	__tablename__ = 'projects'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	description = db.Column(db.Text)
	img_folder = db.Column(db.String(32))
	img_file = db.Column(db.String(32))
	url = db.Column(db.String(128))

	def __repr__(self):
		return '%r'% self.title

class Email(db.Model):
	__tablename__ = 'emails'
	id = db.Column(db.Integer, primary_key=True)
	sender_name = db.Column(db.String(64))
	sender_address = db.Column(db.String(64))
	subject = db.Column(db.String(32))
	content = db.Column(db.Text)

class Email_form(Form):
	name = StringField('name', validators=[Required()])
	email = StringField('email', validators=[Required()])
	subject = StringField('subject')
	body = TextAreaField('text', validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/work')
def work():
	projects = Project.query.all()
	return render_template('work.html', projects=projects)

@app.route('/detail/<id>')
def detail(id):
	project = Project.query.filter_by(id=id).first()
	return render_template('work01.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = Email_form()
	if form.validate_on_submit():
		session['sender_name'] = form.name.data
		session['sender_address'] = form.email.data
		session['subject'] = form.subject.data
		session['content'] = form.body.data

		mail = Email(sender_name=session.get('sender_name'),
					 sender_address=session.get('sender_address'),
					 subject=session.get('subject'),
					 content=session.get('content'))
		db.session.add(mail)
		db.session.commit()
		flash('Form submitted')
		return redirect(url_for('contact'))

	return render_template('contact.html', form=form)

if __name__ == '__main__':
	manager.run()