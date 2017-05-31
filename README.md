# Loan Applications API

REST API for integration with loan application frontends built by client IT
departments.

## Getting Started

### Prerequisites

This API requires the following dependencies be installed.

- python 3
- [mongodb](https://www.mongodb.com/)

Assuming those are installed, you can install the remaining python package dependencies by going into this directory in your terminal and typing the following:

```
pip install -r pip-requirements.txt
```

### Running the API

In order to get the API up and running type the following line in your terminal:

```
python rest_api.py
```

In a new window, type:

```
mongod
```

You can now use the API to do loan applications!

### Using the API

You can POST, GET, PATCH or DELETE with this API.

#### POST example

Applications must have the following types and keys. Anything that
does not have the correct types or keys is considered invalid.

```
{
  "age": <int>,
  "income": <float>,
  "employed": <boolean>
}
```

To POST an application, use the /loanapp route. Here's an example using localhost:

```
curl -H "Content-Type: application/json" -X POST -d '{"age": 22, "income": 27000,"employed": true}' http://localhost:5000/loanapp
```

#### GET example

Having an id, you can GET the application by using the /loanapp/<specialid> route. Here's an example:

```
curl http://localhost:5000/loanapp/592e8baecf1a4804851e0c82
```

#### PATCH example

Updates must have the following types and keys. Anything that
does not have the correct types or keys is considered invalid.

```
{
  "age": <int>
}
```

If you wish to update an age of an applicant in the database, you can send a PATCH to the /loanapp/<specialid> route. Here's an example:

```
curl -H "Content-Type: application/json" -X PATCH -d '{"age": 23}' http://localhost:5000/loanapp/592e8baecf1a4804851e0c82
```

The API will return a JSON response telling you if the PATCH was successful.

#### DELETE example

Finally, to remove an application from the database, just send a DELETE to the /loanapp/<specialid> route. Here's an example:

```
curl -X DELETE http://localhost:5000/loanapp/592e8baecf1a4804851e0c82
```

The API will return a JSON response telling you if the DELETE was successful.

## Testing

The testing script of this API can be found in the directory /features/steps/. In order to test the API, just run:

```
behave
```
