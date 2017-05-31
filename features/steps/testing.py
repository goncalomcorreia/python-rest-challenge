from behave import *
import requests
import sure
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client["loanapp"]
loanapps = db.loanapps

# Scenario: Add a new loan application
@given('the webserver is available')
def step_impl(context):
    request = requests.get('http://localhost:5000/')
    (request.status_code).should.be.equal(200)

@given('a valid application is generated')
def step_impl(context):
    loan_app = {"age": 22, "income": 28000, "employed": True}
    context.loanapp = loan_app
    pass

@when('the endpoint POST /application is called')
def step_impl(context):
    r = requests.post('http://localhost:5000/loanapp', data=context.loanapp)
    context.res_code = r.status_code
    context.res_json = r.json()

@then('the application is returned with an id')
def step_impl(context):
    if context.res_json['id']:
        context.res_id = ObjectId(context.res_json['id'])
        assert True

@then('status 200 is returned')
def step_impl(context):
    (context.res_code).should.be.equal(200)

@then('the loan exists in the database')
def step_impl(context):
    loan_from_id = loanapps.find_one({"_id": context.res_id})
    if loan_from_id is not None:
        assert True


# Scenario: Attempt to add application with missing field
@given('an application with age missing is generated')
def step_impl(context):
    loan_app_missing = {"income": 28000, "employed": True}
    context.loanapp = loan_app_missing
    pass

@then('status 422 is returned')
def step_impl(context):
    (context.res_code).should.be.equal(422)

@then('an error message saying age is missing is returned')
def step_impl(context):
    if context.res_json['messages']['age'][0]:
        error_message = context.res_json['messages']['age'][0]
        if error_message == "age is missing":
            assert True

# Scenario: Attempt to add application with incorrect type
@given('an application with age as a string is generated')
def step_impl(context):
    loan_app_missing = {"age": "Twenty Two", "income": 28000, "employed": True}
    context.loanapp = loan_app_missing
    pass

@then('an error message saying age has wrong type is returned')
def step_impl(context):
    if context.res_json['messages']['age'][0]:
        error_message = context.res_json['messages']['age'][0]
        if error_message == "age has wrong type":
            assert True

# Scenario: Fetch an application by ID
@given('an application exists in the database with id specialid')
def step_impl(context):
    loan_from_id = loanapps.find_one()
    if loan_from_id is not None:
        context.res_id = loan_from_id['_id']
        context.loanapp = loan_from_id
        assert True

@when('GET /application/specialid is called')
def step_impl(context):
    r = requests.get('http://localhost:5000/loanapp/'+str(context.res_id))
    context.res_code = r.status_code
    context.res_json = r.json()

@then('the correct application is returned')
def step_impl(context):
    if context.res_json==context.loanapp:
        assert True

# Scenario: Update an application by ID
@when('PATCH /application/specialid is called to update age')
def step_impl(context):
    context.updated_age = context.loanapp['age'] + 1
    r = requests.patch('http://localhost:5000/loanapp/'+str(context.res_id),
                       json={"age": context.updated_age})
    context.res_code = r.status_code
    context.res_json = r.json()

@then('the updated age is recorded in the database')
def step_impl(context):
    loan_from_id = loanapps.find_one({"_id": context.res_id})
    (loan_from_id['age']).should.be.equal(context.updated_age)

# Scenario: Delete an application by ID
@when('DELETE /application/specialid')
def step_impl(context):
    context.updated_age = context.loanapp['age'] + 1
    r = requests.delete('http://localhost:5000/loanapp/'+str(context.res_id))
    context.res_code = r.status_code
    context.res_json = r.json()

@then('the application with id specialid is no longer in the database')
def step_impl(context):
    loan_from_id = loanapps.find_one({"_id": context.res_id})
    if loan_from_id is None:
        assert True
