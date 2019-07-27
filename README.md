# Screenly OSE API Client

[![image](https://img.shields.io/pypi/v/screenly_ose.svg)](https://pypi.python.org/pypi/screenly_ose) [![image](https://img.shields.io/travis/burnnat/screenly_ose.svg)](https://travis-ci.org/burnnat/screenly_ose)

Library to enable control of Screenly OSE digital signage via [REST API](http://ose.demo.screenlyapp.com/api/docs/).

  - Free software: MIT license

## Sample Usage
```python
import asyncio
import aiohttp
import screenly_ose

async def run():
    async with aiohttp.ClientSession() as session:
        screenly = screenly_ose.Screenly(session, '192.168.1.112')
        asset = await screenly.get_current_asset()
        print(asset)

asyncio.run(run())
```

## API
### Constructor

  - `Screenly(websession, hostname, port=80, encryption=False, timeout=None)`
    
    Creates a new connection to a Screenly OSE instance running on the given hostname and port.

### Methods

All instance methods return `False` in the event of a request error.

  - `get_current_asset()`
    
    Returns a dict containing the following info about the asset currently being displayed:
    
    - `id` The asset ID
    - `name` The asset name
    - `type` The asset type

  - `next_asset()`
  
    Requests Screenly to display the next asset in the sequence.
    
  - `previous_asset()`
  
    Requests Screenly to display the previous asset in the sequence.
    
  - `switch_asset(asset_id)`
  
    Requests Screenly to display the asset with the given ID string.

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
