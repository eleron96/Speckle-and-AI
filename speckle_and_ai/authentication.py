# authentication.py
from specklepy.api.credentials import get_default_account
from .config import client


def authenticate_client():
    account = get_default_account()
    client.authenticate_with_account(account)
