from flask import Flask, request, jsonify
from webargs import fields, validate
from webargs.flaskparser import use_args
import json
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient()
db = client["loanapp"]
loanapps = db.loanapps
app = Flask(__name__)


loan_args = {
    "age": fields.Int(validate=lambda val: val > 0, required=True),
    "income": fields.Float(validate=lambda val: val >= 0, required=True),
    "employed": fields.Bool(required=True)
}


def create(loan_app):
    applied_loan = loanapps.insert_one(loan_app)
    response = {}
    response['id'] = str(loan_app['_id'])
    response['age'] = loan_app['age']
    response['income'] = loan_app['income']
    response['employed'] = loan_app['employed']
    return jsonify(response)


def get_from_id(specialid):
    loan_from_id = loanapps.find_one({"_id": specialid})
    response = {}
    response['id'] = str(loan_from_id['_id'])
    response['age'] = loan_from_id['age']
    response['income'] = loan_from_id['income']
    response['employed'] = loan_from_id['employed']
    return jsonify(response)


def update_id(specialid, update_info):
    updated_loan = loanapps.update_one(
        {'_id': specialid},
        {'$set': {'age': update_info['age']}
         }, upsert=False)
    if updated_loan.modified_count == 1:
        return json.dumps({'success': True}),
        200,
        {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}),
        200,
        {'ContentType': 'application/json'}


def delete_id(specialid):
    response = loanapps.delete_one({"_id": specialid})
    loan_from_id = loanapps.find_one({"_id": specialid})
    if loan_from_id is None:
        return json.dumps({'success': True}),
        200,
        {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}),
        200,
        {'ContentType': 'application/json'}


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    # webargs attaches additional metadata to the `data` attribute
    exc = getattr(err, 'exc')
    if exc:
        # Get validations from the ValidationError object
        messages = exc.messages
    else:
        messages = ['Invalid request']

    if messages['age']:
        original_message = messages['age'][0]
        if original_message == "Not a valid integer.":
            message = "age has wrong type"
            messages['age'] = [message]
        if original_message == "Missing data for required field.":
            message = "age is missing"
            messages['age'] = [message]
    return jsonify({'messages': messages}), 422


@app.route('/')
def home():
    return """POST to /loanapp your application loan.\n
    GET, PATCH or DELETE to /loanapp/specialid if you have a special ID."""


@app.route('/loanapp', methods=['POST'])
@use_args(loan_args)
def create_loan_app(loan_args):
    return create(loan_args)


@app.route('/loanapp/<specialid>', methods=['GET', 'PATCH', 'DELETE'])
def handle_loan_specialid(specialid):
    specialid = ObjectId(specialid)
    if request.method == 'GET':
        return get_from_id(specialid)
    elif request.method == 'PATCH':
        update_info = request.get_json(force=True)
        return update_id(specialid, update_info)
    elif request.method == 'DELETE':
        return delete_id(specialid)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
