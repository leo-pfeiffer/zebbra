# Integration Guide



## Adding a new integration

> To facilitate the implementation process, we provide a script to generate starter files from templates. To get started simply run `make genereate_from_template INTEGRATION=<integration_name>` from the `server` directory.

### 1. Extending the `IntegrationProvider` type
The `IntegrationProvider` type is used across Zebbra as a type for valid integration provider names. To add a new provider, add its name to the `IntegrationProvider` variable in `core/schemas/integrations.py`. Note that the name must be strictly alphanumeric (i.e. `[A-Za-z0-9]+`).

### 2. Adding OAuth connector class
Secondly, you need to set up the OAuth authorization functionality for the OAuth app you want to integrate. Zebbra provides a framework for this with the abstract class `IntegrationOAuth`, which you can override to set up the workflow.

To set up a new integration workflow, create a new file in `core/integrations/oauth` with a class that inherits from `core.integrations.oauth.integration_oauth.IntegrationOAuth`. You will need to implement at least the following methods.

- Override the `__init__` method. Make sure to end the method with a call to the constructor of the superclass (`super().__init__()`).
- Define the class variable `_integration`, which should be the name of your integration as defined in the `IntegrationProvider` type. You will also need to override the getter method `integration(cls)` classmethod, which simply returns the `_integration` variable.
- Override `_perform_token_refresh(...)`.  This method defines the refresh workflow for a token refresh for apps that have been authenticated before, but whose access token has expired. The method is highly dependent on the integration you're integrating. In general, however, the method should call the refresh URL of the OAuth app and update the existing OAuth token information with the new one.
- Override `_store_oauth_token(...)`. This method stores the OAuth token information as an `IntegrationAccess` object in the  database. This is a relatively simple operation, but can depend on the specific OAuth app.

When you set up your OAuth app on the side of the provider,  you will be asked to provide the Callback URL, to which the OAuth server redirects you to after authorization. `IntegrationOAuth` autogenerates these URLs following the pattern `http://<host>/integration/<integration_name>/callback`.  Note that the integration name is put to lower case. 

Similarly, `IntegrationOAuth` autogenerates the URL that your client can call to perform the login to the OAuth app. The login URL follows the pattern `http://<host>/integration/<integration_name>/login`.

Now, create an instance of this class in the same file, which will be used by other parts of the application as appropriate. On this instance, call the `register_oauth_app` method, which is used to configure the OAuth app through the authlib starlette client. The method takes the same arguments as  
`authlib.integrations.starlette_client.OAuth.register`.
See the [authlib documentation](https://docs.authlib.org/en/v0.13/client/frameworks.html#using-oauth-2-0-to-log-in) for details on what to pass to the method.  After registering, the OAuth app is available as an instance variable as  
IntegrationAccess.oauth_app.

Lastly, you need to create the FastAPI routes for the OAuth login and callback. The body of these functions is already implemented in `IntegrationOAuth`, you only have to define the routes using the instance created in the previous step. Assuming your instance is called `xxx`, add the following to the bottom of the file:

```python
@xxx.router.get(**xxx.login_endpoint())  
async def login_route(  
    workspace_id: str,  
    request: Request,  
    current_user: User = Depends(get_current_active_user_url),  
):  
    return await xxx.oauth_login(workspace_id, request, current_user)
  
  
@xxx.router.get(**xxx.callback_endpoint())  
async def callback_route(request: Request):  
    return await xxx.oauth_callback(request)
```

> It is recommended to use the code generator script described above to generate this starter file automatically.

3. Adding fetch adapter
Override `FetchAdapter` from `core/integrations/adapters/adapter.py` and implement abstract methods.

> It is recommended to use the code generator script described above to generate this starter file automatically.

4. Update config
Add registration and router callls to `core/integrations/config.py`
