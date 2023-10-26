# config.py
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account

# Replace the following variables with your data
HOST = 'https://speckle.xyz/'
STREAM_ID = 'f378cb19eb'

# STREAM_ID = 'a531e8ec43'

# Create and authenticate the client
client = SpeckleClient(host=HOST)
account = get_default_account()
client.authenticate_with_account(account)
