from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand



# Database Configurations
app = Flask(__name__)
DATABASE = 'TESTDB'
PASSWORD = 'password'
USER = 'root'
HOSTNAME = 'mysqlserver'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)

# Database migration command line
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Expenses(db.Model):

	# Data Model Expenses Table
	__tablename__ = 'expenses'
	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column('name', db.String(50))
	email = db.Column('email', db.String(100))
	category = db.Column('category', db.String(50))
	description = db.Column('description', db.String(150))
	link = db.Column('link', db.String(200))
	estimated_costs = db.Column('estimated_costs', db.String(10))
	status = db.Column('status', db.String(30))
	submit_date = db.Column('submit_date', db.String(10))
	decision_date = db.Column('decision_date', db.String(10))

	def __init__(self, name = '', email = '', category = '', description = '', link = '', estimated_costs = '', status = '', submit_date = '09/09/09'):
		# initialize columns
		self.name = name
		self.email = email
		self.category = category
		self.description = description
		self.status = status
		self.link = link
		self.estimated_costs = estimated_costs
		self.status = status
		self.submit_date = submit_date

	def __repr__(self):
		return '<Expenses %r>' % self.name

class CreateDB():
	def __init__(self, hostname=None):
		if hostname != None:	
			HOSTNAME = hostname
		import sqlalchemy
		engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
		engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db

if __name__ == '__main__':
	manager.run()
