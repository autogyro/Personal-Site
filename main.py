from flask import Flask, render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import os
from pprint import pprint

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
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
	subject = db.Column(db.Text)
	content = db.Column(db.Text)

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

if __name__ == '__main__':
	manager.run()