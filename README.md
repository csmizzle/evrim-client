[![codecov](https://codecov.io/gh/csmizzle/evrim-client/graph/badge.svg?token=E2V35OBJCA)](https://codecov.io/gh/csmizzle/evrim-client)

# Evrim Client
A simple Python client to interact with [Evrim's](https://www.evrim.ai/) REST API.

## Authentication
Evrim's REST API uses [JSON Web Tokens](https://jwt.io/introduction) (JWT) for authentication. Users can either obtain one using their username and password or use an existing **valid** JWT.

### Username/Password Authentication
Let's start by obtaining a JWT using our username and password. When initializing `Evrim`, the client will authenticate using the provided url, username, and password and obtain a valid JWT.

```python
from evrim import Evrim
import os

# access env variables
url = os.getenv("EVRIM_URL")
username = os.getenv("EVRIM_USERNAME")
password = os.getenv("EVRIM_PASSWORD")

# authenticate using url, username, and password
client = Evrim(
    url=url
    username=username,
    password=password
)
```

If this authentication is successful, two tokens are then issued to the user:
- `access`: Bearer token used in all subsequent requests in the `Authorization` header
- `refresh`: Token used to obtain a new `access` token once it expires

### Token Validation
JWTs expire after a certain amount of time. To check if your token is still valid, `Evrim` provides the `validate_token` function.

```python
from evrim import Evrim
from time import sleep
import os

# access env variables
url = os.getenv("EVRIM_URL")
username = os.getenv("EVRIM_USERNAME")
password = os.getenv("EVRIM_PASSWORD")

# authenticate using url, username, and password
client = Evrim(
    url=url
    username=username,
    password=password
)

# let some time pas
print("sleeping for 20 seconds ...")
sleep(20)

# check if token still valid
if client.validate_token():
    print("Token is still valid!")
```

If your token is still valid, this function will return `True`.


### Token Refresh
If your token happens to be no longer valid, there are a few paths forward:
- Obtain a new JWT using `set_token`
- Refresh your existing token pair with `refresh_token`

Let's look at both in the example below.

#### Set New Tokens
You can set a new token pair by simply using the `set_token` function. This will use your existing username and password to obtain a new token pair.

```python
client.set_token()
```

This will update the session `Authentication` header with your fresh `access` token and set a new `refresh` token.

#### Refresh Existing Token
You can also refresh your existing `access` token using the `refresh_token` function.

```python
client.refresh_token()
```

This will updated only the session `Authorization` header with your fresh `access` token.

### Existing Valid JWT Authentication
We can also authenticate using an existing valid JWT.

```python
from evrim import Evrim
import os

url = os.getenv("EVRIM_URL")
token = os.getenv("EVRIM_TOKEN")
refresh = os.getenv("EVRIM_REFRESH_TOKEN")  # optional but can be used to refresh existing access token

client = Evrim.from_token(
    url=url,
    token=token,
    refresh=refresh  # optional value but helpful!
)
```

This is will do two things:
- Validate your access token to ensure it is still valid
- If valid, set you session `Authorization` header with the existing valid `access` token
- If `response` is provided, this token will also be set so you can leverage operations like `refresh_token`.


## Contact
Please reach out to chris@evrim.ai with any feedback or ideas!
