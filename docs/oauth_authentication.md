# OAuth 2.0 Authentication

## Getting an access token

```python
import requests

r = requests.post(
        'http://localhost:8000/token', 
        data={
            'username': 'johndoe@example.com', 
            'password': 'secret'
        }
    )

print(r.json())

# {
#   'access_token': 'eyJhbGciO...', 
#   'token_type': 'bearer'
# }
```

## Using the access token

```python
r = requests.get(
    "http://localhost:8000/user", 
    headers={
        "Authorization": f"Bearer eyJhbGciO..."
    }
)

print(r.json())

# {
#     '_id': '62bb11835529faba0704639d', 
#     'username': 'johndoe@example.com', 
#     'first_name': 'John', 
#     'last_name': 'Doe', 
#     'workspaces': [
#         {
#             '_id': '62bc5706a40e85213c27ce29', 
#             'name': 'ACME Inc.'
#         }
#     ], 
#     'models': [
#         {
#             '_id': '62b488ba433720870b60ec0a', 
#             'name': 'model1'
#         }
#     ]
# }
```

## Checking for token expiry

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
