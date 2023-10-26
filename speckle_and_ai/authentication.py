# authentication.py
from config import client
from specklepy.api.credentials import get_default_account

def authenticate_client():
    account = get_default_account()
    client.authenticate_with_account(account)
