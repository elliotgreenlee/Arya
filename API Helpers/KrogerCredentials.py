from datetime import datetime, timezone
import json
from Utils.utils import load_json


class KrogerCredentials:
    def __init__(self, client_id, client_secret, scopes,
                 token=None, refresh_token=None, token_type=None, expiry=None):
        self.client_id = client_id
        self.client_secret = client_secret

        self.cart_scope = scopes['cart_scope']
        self.locations_scope = scopes['locations_scope']
        self.products_scope = scopes['products_scope']
        self.profile_scope = scopes['profile_scope']

        self.token = token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expiry = expiry

        self.user_credentials_path = None

    @property
    def expired(self):
        if self.expiry:
            now = datetime.now(timezone.utc)
            return now >= self.expiry
        else:
            return True

    @classmethod
    def from_authorized_user_file(cls, user_credentials_path, scopes=None):
        user_credentials = load_json(user_credentials_path)
        token = user_credentials['token']
        refresh_token = user_credentials['refresh_token']
        expiry = user_credentials['expiry']
        token_type = user_credentials['token_type']
        client_id = user_credentials['client_id']
        client_secret = user_credentials['client_secret']

        if scopes is None:
            scopes = {
                "cart_scope": user_credentials['cart_scope'],
                "locations_scope": user_credentials['locations_scope'],
                "products_scope": user_credentials['products_scope'],
                "profile_scope": user_credentials['profile_scope'],
            }

        if expiry:
            expiry = datetime.strptime(
                expiry.rstrip("Z").split(".")[0], "%Y-%m-%dT%H:%M:%S"
            )

        kroger_creds = cls(
            token=token,
            refresh_token=refresh_token,
            token_type=token_type,
            expiry=expiry,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes
        )
        kroger_creds.user_credentials_path = user_credentials_path
        return kroger_creds

    def to_json(self):
        prep = {
            "token": self.token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "cart_scope": self.cart_scope,
            "locations_scope": self.locations_scope,
            "products_scope": self.products_scope,
            "profile_scope": self.profile_scope,
        }
        if self.expiry:  # flatten expiry timestamp
            prep["expiry"] = self.expiry.isoformat() + "Z"

        return json.dumps(prep)

    def refresh(self):
        """Refreshes the access token"""
        # TODO: do it
        self.token = ""
