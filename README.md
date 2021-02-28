# smite-api
Simple Smite API wrapper written in Python

## How to use
You can either run the provided flask server or include _smite_ folder on your project to write some custom code.

### Examples
Usage is pretty simple. Just create a SmiteAPI instance like this:
```python
from smite.api import SmiteAPI

# Create handler for Smite API
api_handler = SmiteAPI("yourDevId", "yourAuthKey")
```

Before getting any data, you have to retrieve a _session token_ which lasts for 15 minutes.
```python
# Get and store a new session token
api_handler.get_session_token()
```

You have to get a new token every 15 minutes, so in order to avoid that you can use the following instead:
```python
# Create thread to update session token every 15 minutes
api_handler.create_session_token_thread()
```

Either way, you're now ready to get some data and play with it:
```python
# Get all smite gods and print the lore of the first
# retrieved god
all_gods = api_handler.call_generic_method("getgods")
print(all_gods[0]["Lore"])

# Get all skins for god with ID 3492 (Achilles)
all_achilles_skins = api_handler.call_generic_method("getgodskins", [3492])
print(all_achilles_skins[0]["godSkin_URL"])
```

I understand it'd be nice to have something like `api_handler.get_gods()`, `api_handler.get_gods_skins(3492)` (and all others) but honestly at the moment I'm too lazy to add them. Feel free to submit a PR with those and all other available methods (here's their [Smite API docs](https://docs.google.com/document/d/1OFS-3ocSx-1Rvg4afAnEHlT3917MAK_6eJTR6rzr-BM)), it's basically adding a call to `call_generic_method()` with their corresponding names.

### Run the flask server
Install requirements with `pip install -r requirements.txt`

Edit _config.tmp_ and rename to _config.py_:
```python
...
# Hi-Rez Smite API
DEV_ID = "CHANGE_ME"
AUTH_KEY = "CHANGE_ME"
...
```

For testing purposes just run `python server.py`

You might want to [deploy to production](https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/)
