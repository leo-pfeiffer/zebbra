# Zebbra API Docs

> Version 3.0.2

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/](#get) | Root |
| POST | [/auth/token](#postauthtoken) | Login For Access Token |
| GET | [/auth/token/expired](#getauthtokenexpired) | Token Expired Information |
| POST | [/auth/logout](#postauthlogout) | Logout Current User |
| POST | [/auth/register](#postauthregister) | Register New User |
| GET | [/user](#getuser) | Retrieve Current User Info |
| POST | [/user](#postuser) | Update Current User |
| DELETE | [/user](#deleteuser) | Delete Current |
| POST | [/user/otp/create](#postuserotpcreate) | Create Otp Secret For Current User |
| POST | [/user/otp/validate](#postuserotpvalidate) | User Otp Validate |
| GET | [/user/requiresOtp](#getuserrequiresotp) | Check Otp Status Of Current User |
| GET | [/model/meta](#getmodelmeta) | Retrieve Model Meta |
| GET | [/model/users](#getmodelusers) | Retrieve Users With Access To Model |
| POST | [/model/grant](#postmodelgrant) | Grant Permission For Model |
| POST | [/model/revoke](#postmodelrevoke) | Revoke All Permissions For Model |
| POST | [/model/rename](#postmodelrename) | Rename Existing Model |
| POST | [/model/startingMonth](#postmodelstartingmonth) | Set Starting Month Of Model |
| POST | [/model/startingBalance](#postmodelstartingbalance) | Set Starting Balance Of Model |
| POST | [/model/add](#postmodeladd) | Create New Model |
| DELETE | [/model](#deletemodel) | Delete Existing Model |
| GET | [/model/revenues](#getmodelrevenues) | Retrieve Revenues Sheet Of Model |
| POST | [/model/revenues](#postmodelrevenues) | Update Revenues Sheet Of Model |
| GET | [/model/costs](#getmodelcosts) | Retrieve Costs Sheet Of Model |
| POST | [/model/costs](#postmodelcosts) | Update Costs Sheet Of Model |
| GET | [/model/payroll](#getmodelpayroll) | Retrieve Model Payroll |
| POST | [/model/payroll](#postmodelpayroll) | Update Model Payroll |
| GET | [/workspace](#getworkspace) | Get Workspace For User |
| POST | [/workspace](#postworkspace) | Create New Workspace |
| GET | [/workspace/users](#getworkspaceusers) | List Workspace Users |
| POST | [/workspace/rename](#postworkspacerename) | Rename Workspace |
| POST | [/workspace/add](#postworkspaceadd) | Add User To A Workspace |
| POST | [/workspace/remove](#postworkspaceremove) | Remove User From A Workspace |
| POST | [/workspace/changeAdmin](#postworkspacechangeadmin) | Set Admin Of Workspace |
| POST | [/workspace/inviteCode](#postworkspaceinvitecode) | Create Invite Code For Workspace |
| POST | [/integration/disconnect](#postintegrationdisconnect) | Disconnect Integration From Workspace |
| GET | [/integration/providers](#getintegrationproviders) | List Available Integration Providers |
| GET | [/integration/dataEndpoints](#getintegrationdataendpoints) | List Available Data Endpoints |
| GET | [/integration/xero/login](#getintegrationxerologin) | Xero Oauth Login |
| GET | [/integration/gusto/login](#getintegrationgustologin) | Gusto Oauth Login |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| Body_login_for_access_token_auth_token_post | [#/components/schemas/Body_login_for_access_token_auth_token_post](#componentsschemasbody_login_for_access_token_auth_token_post) |  |
| DataPoint | [#/components/schemas/DataPoint](#componentsschemasdatapoint) |  |
| DateValue | [#/components/schemas/DateValue](#componentsschemasdatevalue) |  |
| Employee | [#/components/schemas/Employee](#componentsschemasemployee) |  |
| ExpiredMessage | [#/components/schemas/ExpiredMessage](#componentsschemasexpiredmessage) |  |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |  |
| IntegrationProviderInfo | [#/components/schemas/IntegrationProviderInfo](#componentsschemasintegrationproviderinfo) |  |
| InviteCode | [#/components/schemas/InviteCode](#componentsschemasinvitecode) |  |
| Message | [#/components/schemas/Message](#componentsschemasmessage) |  |
| Model | [#/components/schemas/Model](#componentsschemasmodel) |  |
| ModelInfo | [#/components/schemas/ModelInfo](#componentsschemasmodelinfo) |  |
| ModelMeta | [#/components/schemas/ModelMeta](#componentsschemasmodelmeta) |  |
| ModelUser | [#/components/schemas/ModelUser](#componentsschemasmodeluser) |  |
| OtpUrl | [#/components/schemas/OtpUrl](#componentsschemasotpurl) |  |
| OtpValidation | [#/components/schemas/OtpValidation](#componentsschemasotpvalidation) |  |
| Payroll | [#/components/schemas/Payroll](#componentsschemaspayroll) |  |
| RegisterUser | [#/components/schemas/RegisterUser](#componentsschemasregisteruser) |  |
| Row | [#/components/schemas/Row](#componentsschemasrow) |  |
| Section | [#/components/schemas/Section](#componentsschemassection) |  |
| Sheet | [#/components/schemas/Sheet](#componentsschemassheet) |  |
| SheetMeta | [#/components/schemas/SheetMeta](#componentsschemassheetmeta) |  |
| Token | [#/components/schemas/Token](#componentsschemastoken) |  |
| UpdateEmployee | [#/components/schemas/UpdateEmployee](#componentsschemasupdateemployee) |  |
| User | [#/components/schemas/User](#componentsschemasuser) |  |
| UserInfo | [#/components/schemas/UserInfo](#componentsschemasuserinfo) |  |
| ValidationError | [#/components/schemas/ValidationError](#componentsschemasvalidationerror) |  |
| Workspace | [#/components/schemas/Workspace](#componentsschemasworkspace) |  |
| WorkspaceInfo | [#/components/schemas/WorkspaceInfo](#componentsschemasworkspaceinfo) |  |
| WorkspaceUser | [#/components/schemas/WorkspaceUser](#componentsschemasworkspaceuser) |  |
| OAuth2PasswordBearer | [#/components/securitySchemes/OAuth2PasswordBearer](#componentssecurityschemesoauth2passwordbearer) |  |
| OAuth2PasswordBearerURL | [#/components/securitySchemes/OAuth2PasswordBearerURL](#componentssecurityschemesoauth2passwordbearerurl) |  |

## Path Details

***

### [GET]/

- Summary  
Root

- Description  
Heartbeat endpoint to check if server is running.

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

***

### [POST]/auth/token

- Summary  
Login For Access Token

- Description  
Get an OAuth access token using the user's credentials.

#### RequestBody

- application/x-www-form-urlencoded

```ts
{
  grant_type?: string
  username: string
  password: string
  scope?: string
  client_id?: string
  client_secret?: string
  otp?: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  access_token: string
  token_type: string
}
```

- 401 Incorrect username or password

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/auth/token/expired

- Summary  
Token Expired Information

- Description  
Get information if the token is expired or not.

- Security  
OAuth2PasswordBearer  

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  expired: boolean
}
```

***

### [POST]/auth/logout

- Summary  
Logout Current User

- Description  
Logout the user who is currently logged in. This invalidates the access  
token.

- Security  
OAuth2PasswordBearer  

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

***

### [POST]/auth/register

- Summary  
Register New User

- Description  
Register a new user. To add the user to an existing workspace, specify the  
workspace_id. To create a new workspace with the user as admin, specify  
new_workspace_name. You cannot specify both.

#### RequestBody

- application/json

```ts
{
  username: string
  first_name: string
  last_name: string
  invite_code?: string
  new_workspace_name?: string
  password: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  username: string
  first_name?: string
  last_name?: string
  disabled?: boolean
}
```

- 409 Username or workspace already exists

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/user

- Summary  
Retrieve Current User Info

- Description  
Retrieve current user's data.

- Security  
OAuth2PasswordBearer  

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id: string
  username: string
  first_name?: string
  last_name?: string
  workspaces: {
    _id: string
    name: string
  }[]
  models: {
    _id: string
    name: string
  }[]
}
```

***

### [POST]/user

- Summary  
Update Current User

- Description  
Update the current user.  
    username: New username (e-mail address)  
    first_name: New first name  
    last_name: New last name  
    password: New password

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
username?: string
```

```ts
first_name?: string
```

```ts
last_name?: string
```

```ts
password?: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  username: string
  first_name?: string
  last_name?: string
  disabled?: boolean
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [DELETE]/user

- Summary  
Delete Current

- Description  
Delete a user's account. This requires that the user is not  
admin of any workspace, model etc.

- Security  
OAuth2PasswordBearer  

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 400 Attempting to delete admin.

***

### [POST]/user/otp/create

- Summary  
Create Otp Secret For Current User

- Description  
Create an OTP secret for the user. If the user already has an OTP secret,  
the old one will be overridden.

- Security  
OAuth2PasswordBearer  

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  url: string
  secret: string
  issuer: string
  name: string
}
```

***

### [POST]/user/otp/validate

- Summary  
User Otp Validate

- Description  
Validate an OTP.  
    otp: The OTP to validate.

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
otp: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  otp: string
  valid: boolean
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/user/requiresOtp

- Summary  
Check Otp Status Of Current User

- Description  
Check if the user requires an OTP.  
    username: The username of the user.

#### Parameters(Query)

```ts
username: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/model/meta

- Summary  
Retrieve Model Meta

- Description  
Retrieve metadata of a model.  
  
    model_id: Id of the model whose meta data to retrieve

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  name: string
  admins?: string[]
  editors?: string[]
  viewers?: string[]
  workspace: string
  starting_month: string
  starting_balance?: number
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/model/users

- Summary  
Retrieve Users With Access To Model

- Description  
Retrieve a list of users that can access a model.  
  
    model_id: ID of the model whose users to retrieve

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id: string
  username: string
  first_name?: string
  last_name?: string
  user_role: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/grant

- Summary  
Grant Permission For Model

- Description  
Grant a permission to a user for a model.  
  
    model_id: Model for which to give permission to  
    role: Permission to be granted ["admin", "editor", "viewer"]  
    user_id: User to whom the permission is granted

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

```ts
role: string
```

```ts
user_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/revoke

- Summary  
Revoke All Permissions For Model

- Description  
Revoke all permissions from a user for a model.  
  
    model_id: Model for which to revoke permission from  
    user_id: User from whom the permission is revoked

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

```ts
user_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/rename

- Summary  
Rename Existing Model

- Description  
Rename a model.  
  
    model_id: Model to rename  
    name: The new name for the model

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

```ts
name: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/startingMonth

- Summary  
Set Starting Month Of Model

- Description  
Set the starting month of a model. The starting month is provided as a date  
  
    model_id: Model whose starting month to change  
    starting_month: New starting month

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

```ts
starting_month: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/startingBalance

- Summary  
Set Starting Balance Of Model

- Description  
Set the starting balance of a model.  
  
    model_id: Model whose starting balance to change  
    starting_balance: New starting month

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

```ts
starting_balance: number
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/add

- Summary  
Create New Model

- Description  
Create a new model with the current user as admin.  
  
    name: Name of the new model  
    workspace_id: ID of the workspace to which the workspace belongs

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
name: string
```

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  meta: {
    name: string
    admins?: string[]
    editors?: string[]
    viewers?: string[]
    workspace: string
    starting_month: string
    starting_balance?: number
  }
  sheets: {
    meta: {
      name: string
    }
    assumptions: {
      _id?: string
      name: string
      val_type: string
      editable: boolean
      var_type: string
      time_series: boolean
      starting_at: integer
      first_value_diff: boolean
      value: string
      integration_name?: string
      value_1?: string
      integration_values: {
        date: string
        value?: string
      }[]
      decimal_places?: integer
    }[]
    sections: {
      name: string
      rows:#/components/schemas/Row[]
      end_row:#/components/schemas/Row
    }[]
  }[]
  payroll: {
    payroll_values:#/components/schemas/DateValue[]
    employees: {
      _id?: string
      name?: string
      start_date: string
      end_date?: string
      title?: string
      department?: string
      monthly_salary: integer
      from_integration: boolean
    }[]
  }
}
```

- 400 Workspace does not exist.

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [DELETE]/model

- Summary  
Delete Existing Model

- Description  
Delete an existing model  
  
    model_id: Id of the model to be deleted.

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 400 Model does not exist.

- 403 User is not admin.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/model/revenues

- Summary  
Retrieve Revenues Sheet Of Model

- Description  
Retrieve the 'Revenues' sheet of a model.  
  
    model_id: Model for which to retrieve the sheet

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  meta: {
    name: string
  }
  assumptions: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  sections: {
    name: string
    rows:#/components/schemas/Row[]
    end_row:#/components/schemas/Row
  }[]
}
```

- 400 Model does not exist.

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/revenues

- Summary  
Update Revenues Sheet Of Model

- Description  
Update the 'Revenues' sheet of a model.  
  
    model_id: Model for which to update the sheet  
    sheet_data: New data of the sheet

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### RequestBody

- application/json

```ts
{
  meta: {
    name: string
  }
  assumptions: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  sections: {
    name: string
    rows:#/components/schemas/Row[]
    end_row:#/components/schemas/Row
  }[]
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  meta: {
    name: string
  }
  assumptions: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  sections: {
    name: string
    rows:#/components/schemas/Row[]
    end_row:#/components/schemas/Row
  }[]
}
```

- 400 Model does not exist.

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/model/costs

- Summary  
Retrieve Costs Sheet Of Model

- Description  
Retrieve the 'Costs' sheet of a model.  
  
    model_id: Model for which to retrieve the sheet

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  meta: {
    name: string
  }
  assumptions: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  sections: {
    name: string
    rows:#/components/schemas/Row[]
    end_row:#/components/schemas/Row
  }[]
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/costs

- Summary  
Update Costs Sheet Of Model

- Description  
Update the 'Costs' sheet of a model.  
  
    model_id: Model for which to update the sheet  
    sheet_data: New data of the sheet

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### RequestBody

- application/json

```ts
{
  meta: {
    name: string
  }
  assumptions: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  sections: {
    name: string
    rows:#/components/schemas/Row[]
    end_row:#/components/schemas/Row
  }[]
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  meta: {
    name: string
  }
  assumptions: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  sections: {
    name: string
    rows:#/components/schemas/Row[]
    end_row:#/components/schemas/Row
  }[]
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/model/payroll

- Summary  
Retrieve Model Payroll

- Description  
Retrieve the payroll information of a model.  
  
    model_id: Model for which to retrieve the data

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  payroll_values: {
    date: string
    value?: string
  }[]
  employees: {
    _id?: string
    name?: string
    start_date: string
    end_date?: string
    title?: string
    department?: string
    monthly_salary: integer
    from_integration: boolean
  }[]
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/model/payroll

- Summary  
Update Model Payroll

- Description  
Update the payroll information of a model.  
  
    model_id: Model for which to update the payroll  
    employee_data: New data of the payroll employees

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### RequestBody

- application/json

```ts
{
  name?: string
  start_date: string
  end_date?: string
  title?: string
  department?: string
  monthly_salary: integer
  from_integration: boolean
}[]
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  payroll_values: {
    date: string
    value?: string
  }[]
  employees: {
    _id?: string
    name?: string
    start_date: string
    end_date?: string
    title?: string
    department?: string
    monthly_salary: integer
    from_integration: boolean
  }[]
}
```

- 403 User does not have access to the resource.

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/workspace

- Summary  
Get Workspace For User

- Description  
Get all workspaces for the logged-in user.

- Security  
OAuth2PasswordBearer  

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  name: string
  admin: string
  users?: string[]
}[]
```

***

### [POST]/workspace

- Summary  
Create New Workspace

- Description  
Create a new workspace with the current user as admin.  
  
    name: name of the workspace

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
name: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  name: string
  admin: string
  users?: string[]
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/workspace/users

- Summary  
List Workspace Users

- Description  
Get all users for a workspace.  
  
    :workspace_id: ID of the workspace

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id: string
  username: string
  first_name?: string
  last_name?: string
  user_role: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/workspace/rename

- Summary  
Rename Workspace

- Description  
Rename a workspace.  
  
    workspace_id: ID of the workspace to rename.  
    new_name: New name for the workspace.

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
workspace_id: string
```

```ts
new_name: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  name: string
  admin: string
  users?: string[]
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/workspace/add

- Summary  
Add User To A Workspace

- Description  
Add a user to a workspace.  
  
    user_id: ID of the user to add.  
    workspace_id: ID of the workspace to add the user to.

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
user_id: string
```

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  name: string
  admin: string
  users?: string[]
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/workspace/remove

- Summary  
Remove User From A Workspace

- Description  
Remove a user from a workspace.  
  
    user_id: ID of the user to remove.  
    workspace_id: ID of the workspace to remove the user from.

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
user_id: string
```

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  name: string
  admin: string
  users?: string[]
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/workspace/changeAdmin

- Summary  
Set Admin Of Workspace

- Description  
Set another user as admin of a workspace.  
  
    user_id: ID of the user to set as admin.  
    workspace_id: ID of the workspace to set the admin for.

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
user_id: string
```

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  _id?: string
  name: string
  admin: string
  users?: string[]
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/workspace/inviteCode

- Summary  
Create Invite Code For Workspace

- Description  
Create an invite code for a workspace.  
  
    workspace_id: ID of the workspace to create the invite code for.

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  invite_code: string
  workspace_id: string
  expires: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/integration/disconnect

- Summary  
Disconnect Integration From Workspace

- Description  
Disconnects an integration from a workspace.  
    workspace_id: ID of the workspace  
    integration: Integration provider

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
workspace_id: string
```

```ts
integration: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  message: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/integration/providers

- Summary  
List Available Integration Providers

- Description  
Return all integration providers for a workspace including information if the  
integration is connected.  
  
    workspace_id: ID of the workspace

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  name: string
  connected: boolean
  requires_reconnect: boolean
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/integration/dataEndpoints

- Summary  
List Available Data Endpoints

- Description  
Return all endpoints for all integrations available to a workspace.  
  
    model_id: ID of the workspace

- Security  
OAuth2PasswordBearer  

#### Parameters(Query)

```ts
model_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  id: string
  integration: string
  name: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/integration/xero/login

- Summary  
Xero Oauth Login

- Security  
OAuth2PasswordBearerURL  

#### Parameters(Query)

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/integration/gusto/login

- Summary  
Gusto Oauth Login

- Security  
OAuth2PasswordBearerURL  

#### Parameters(Query)

```ts
workspace_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

## References

### #/components/schemas/Body_login_for_access_token_auth_token_post

```ts
{
  grant_type?: string
  username: string
  password: string
  scope?: string
  client_id?: string
  client_secret?: string
  otp?: string
}
```

### #/components/schemas/DataPoint

```ts
{
  id: string
  integration: string
  name: string
}
```

### #/components/schemas/DateValue

```ts
{
  date: string
  value?: string
}
```

### #/components/schemas/Employee

```ts
{
  _id?: string
  name?: string
  start_date: string
  end_date?: string
  title?: string
  department?: string
  monthly_salary: integer
  from_integration: boolean
}
```

### #/components/schemas/ExpiredMessage

```ts
{
  expired: boolean
}
```

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/IntegrationProviderInfo

```ts
{
  name: string
  connected: boolean
  requires_reconnect: boolean
}
```

### #/components/schemas/InviteCode

```ts
{
  invite_code: string
  workspace_id: string
  expires: string
}
```

### #/components/schemas/Message

```ts
{
  message: string
}
```

### #/components/schemas/Model

```ts
{
  _id?: string
  meta: {
    name: string
    admins?: string[]
    editors?: string[]
    viewers?: string[]
    workspace: string
    starting_month: string
    starting_balance?: number
  }
  sheets: {
    meta: {
      name: string
    }
    assumptions: {
      _id?: string
      name: string
      val_type: string
      editable: boolean
      var_type: string
      time_series: boolean
      starting_at: integer
      first_value_diff: boolean
      value: string
      integration_name?: string
      value_1?: string
      integration_values: {
        date: string
        value?: string
      }[]
      decimal_places?: integer
    }[]
    sections: {
      name: string
      rows:#/components/schemas/Row[]
      end_row:#/components/schemas/Row
    }[]
  }[]
  payroll: {
    payroll_values:#/components/schemas/DateValue[]
    employees: {
      _id?: string
      name?: string
      start_date: string
      end_date?: string
      title?: string
      department?: string
      monthly_salary: integer
      from_integration: boolean
    }[]
  }
}
```

### #/components/schemas/ModelInfo

```ts
{
  _id: string
  name: string
}
```

### #/components/schemas/ModelMeta

```ts
{
  name: string
  admins?: string[]
  editors?: string[]
  viewers?: string[]
  workspace: string
  starting_month: string
  starting_balance?: number
}
```

### #/components/schemas/ModelUser

```ts
{
  _id: string
  username: string
  first_name?: string
  last_name?: string
  user_role: string
}
```

### #/components/schemas/OtpUrl

```ts
{
  url: string
  secret: string
  issuer: string
  name: string
}
```

### #/components/schemas/OtpValidation

```ts
{
  otp: string
  valid: boolean
}
```

### #/components/schemas/Payroll

```ts
{
  payroll_values: {
    date: string
    value?: string
  }[]
  employees: {
    _id?: string
    name?: string
    start_date: string
    end_date?: string
    title?: string
    department?: string
    monthly_salary: integer
    from_integration: boolean
  }[]
}
```

### #/components/schemas/RegisterUser

```ts
{
  username: string
  first_name: string
  last_name: string
  invite_code?: string
  new_workspace_name?: string
  password: string
}
```

### #/components/schemas/Row

```ts
{
  _id?: string
  name: string
  val_type: string
  editable: boolean
  var_type: string
  time_series: boolean
  starting_at: integer
  first_value_diff: boolean
  value: string
  integration_name?: string
  value_1?: string
  integration_values: {
    date: string
    value?: string
  }[]
  decimal_places?: integer
}
```

### #/components/schemas/Section

```ts
{
  name: string
  rows: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  end_row:#/components/schemas/Row
}
```

### #/components/schemas/Sheet

```ts
{
  meta: {
    name: string
  }
  assumptions: {
    _id?: string
    name: string
    val_type: string
    editable: boolean
    var_type: string
    time_series: boolean
    starting_at: integer
    first_value_diff: boolean
    value: string
    integration_name?: string
    value_1?: string
    integration_values: {
      date: string
      value?: string
    }[]
    decimal_places?: integer
  }[]
  sections: {
    name: string
    rows:#/components/schemas/Row[]
    end_row:#/components/schemas/Row
  }[]
}
```

### #/components/schemas/SheetMeta

```ts
{
  name: string
}
```

### #/components/schemas/Token

```ts
{
  access_token: string
  token_type: string
}
```

### #/components/schemas/UpdateEmployee

```ts
{
  name?: string
  start_date: string
  end_date?: string
  title?: string
  department?: string
  monthly_salary: integer
  from_integration: boolean
}
```

### #/components/schemas/User

```ts
{
  _id?: string
  username: string
  first_name?: string
  last_name?: string
  disabled?: boolean
}
```

### #/components/schemas/UserInfo

```ts
{
  _id: string
  username: string
  first_name?: string
  last_name?: string
  workspaces: {
    _id: string
    name: string
  }[]
  models: {
    _id: string
    name: string
  }[]
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```

### #/components/schemas/Workspace

```ts
{
  _id?: string
  name: string
  admin: string
  users?: string[]
}
```

### #/components/schemas/WorkspaceInfo

```ts
{
  _id: string
  name: string
}
```

### #/components/schemas/WorkspaceUser

```ts
{
  _id: string
  username: string
  first_name?: string
  last_name?: string
  user_role: string
}
```

### #/components/securitySchemes/OAuth2PasswordBearer

```ts
{
  "type": "oauth2",
  "flows": {
    "password": {
      "scopes": {},
      "tokenUrl": "token"
    }
  }
}
```

### #/components/securitySchemes/OAuth2PasswordBearerURL

```ts
{
  "type": "oauth2",
  "flows": {
    "password": {
      "scopes": {},
      "tokenUrl": "token"
    }
  }
}
```