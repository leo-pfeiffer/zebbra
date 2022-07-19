# OAuth 2.0 Authentication

Zebbra uses the OAuth 2.0 protocol to authenticate the user during requests. In this guide we provide examples of how to make requests to the API using  OAuth authentication.

> You will need to install the Python `requests` module to run the examples

## Registering a new user

To register a new user, you don't need to authenticat yourself. Instead, send the data of the new user to the `/register` endpoint, like so:

```python
import requests
import json

form_data = {
  "username": "charlie_brown@example.com",
  "first_name": "Charlie",
  "last_name": "Brown",
  "new_workspace_name": "My Workspace",
  "password": "secret"
}

r = requests.post(
    "http://localhost:8000/register",
    data=json.dumps(form_data),
)

print(r.json())

# {
#     '_id': '62d6c3de8688a74266d6c464', 
#     'username': 'charlie_brown@example.com',
#     'first_name': 'Charlie', 
#     'last_name': 'Brown', 
#     'workspaces': [
#         {
#             '_id': '62d6c3de8688a74266d6c465', 
#             'name': 'My Workspace'
#         }
#     ], 
#     'models': []
# }

```

You can now use the specified credentials `username = charlie_brown@example.com` and `password = secret` to request and OAuth access token.

## Getting an access token

OAuth access tokens are used to authenticate the user who's sending the request. To get a token, send a POST request to the `/token` endpoint with your credentials in the body, like so:

```python
r = requests.post(
        'http://localhost:8000/token', 
        data={
            'username': 'charlie_brown@example.com', 
            'password': 'secret'
        }
    )

print(r.json())

# {
#   'access_token': 'eyJhbGciO...', 
#   'token_type': 'bearer'
# }
```

Use the `access_token` returned in the response in future requests.

## Using the access token

For example, the user can access the `/user` endpoint to retrieve user information about themselves. To use the OAuth access token, add an authorization header with the access token from the previous step, like so:

```python
r = requests.get(
    "http://localhost:8000/user", 
    headers={
        "Authorization": f"Bearer eyJhbGciO..."
    }
)

print(r.json())

# {
#     '_id': '62d6c3de8688a74266d6c464', 
#     'username': 'charlie_brown@example.com', 
#     'first_name': 'Charlie', 
#     'last_name': 'Brown', 
#     'workspaces': [], 
#     'models': []
# }
```

## Checking for token expiry

For security reasons, access tokens expire after 30 minutes. If you use an expired access token, the authentication will not succeed. Thus, to determine if your current access token is still valid, you can send a GET request to the `/token/expired` endpoint.

```python
r = requests.get(
    "http://localhost:8000/token/expired", 
    headers={
        "Authorization": f"Bearer eyJhbGciO..."
    }
)

print(r.json())

# {
#     'expired': False
# }
```

In this case, the token is not yet expired. If `'expired': True`, you have to request a new access token from the `/token` endpoint, as previously seen.
