from flask import Flask, jsonify
from flask import request
from model import db
from model import Expenses
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os

# initate flask app
app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello World! Docker-Compose for Flask & Mysql\n'

@app.route("/v1/expenses", methods=['POST'])
def post():
    CreateDB(hostname='mysqlserver')
    db.create_all()

    data = request.get_json(force=True)
    name = data['name']
    email = data['email']
    category = data['category']
    description = data['description']
    link = data['link']
    estimated_costs = data['estimated_costs']
    submit_date = data['submit_date']
    status = 'pending'
    new_row = Expenses(name, email, category, description, link, estimated_costs, status, submit_date)
    db.session.add(new_row)
    db.session.commit()
    id = Expenses.query.order_by(Expenses.id.desc()).first().id
    response = {
        'id': id,
        'name': name,
        'email': email,
        'category': category,
        'description': description,
        'link': link,
        'estimated_costs': estimated_costs,
        'submit_date': data['submit_date'],
        'status': status,
        'decision_date': ""
    }
    return (jsonify(response), 201)


@app.route('/v1/expenses/<int:request_id>', methods=['GET'])
def get_request(request_id):
    request_row = Expenses.query.filter_by(id=request_id).first()
    if (request_row != None):
        id = request_row.id
        name = request_row.name
        email = request_row.email
        category = request_row.category
        description = request_row.description
        link = request_row.link
        estimated_costs = request_row.estimated_costs
        submit_date = request_row.submit_date
        status = request_row.status
        decision_date = request_row.decision_date
        if decision_date == None:
            decision_date = ""

        response = {
            'id': id,
            'name': name,
            'email': email,
            'category': category,
            'description': description,
            'link': link,
            'estimated_costs': estimated_costs,
            'submit_date': submit_date,
            'status': status,
            'decision_date': decision_date
        }

        return jsonify(response)

    else:
        return "Request Not Found", 404


@app.route('/v1/expenses/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    data = request.get_json(force=True)
    update_row = db.session.query(Expenses).filter_by(id=request_id)
    for key, value in data.items():
        update_row.update({key: value})
    db.session.commit()
    return ("Your request has been updated", 202)

@app.route('/v1/expenses/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    db.session.query(Expenses).filter_by(id=request_id).delete()
    db.session.commit()
    return ("Your request has been deleted", 204)
@app.before_first_request
def createDatabase():
	database = CreateDB(hostname = 'mysqlserver')
	db.create_all()
	print ("Database and table created")

# run app service 
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)

