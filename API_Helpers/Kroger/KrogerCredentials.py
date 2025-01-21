from datetime import datetime, timezone
import json
from Utils.utils import load_json
from requests_oauthlib import OAuth2Session


class KrogerCredentials:
    def __init__(self, client_id, client_secret, scope,
                 token=None, refresh_token=None, token_type=None, expiry=None):
        self.client_id = client_id
        self.client_secret = client_secret

        self.scope = scope
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
    def from_authorized_user_file(cls, user_credentials_path, scope=None):
        user_credentials = load_json(user_credentials_path)
        token = user_credentials['token']
        refresh_token = user_credentials['refresh_token']
        expiry = user_credentials['expiry']
        token_type = user_credentials['token_type']
        client_id = user_credentials['client_id']
        client_secret = user_credentials['client_secret']

        if scope is None:
            scope = user_credentials['scope']

        if expiry:
            expiry = datetime.strptime(expiry, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

        kroger_creds = cls(
            token=token,
            refresh_token=refresh_token,
            token_type=token_type,
            expiry=expiry,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope
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
            "scope": self.scope,
        }
        if self.expiry:  # flatten expiry timestamp
            prep["expiry"] = self.expiry.isoformat() + "Z"

        return json.dumps(prep)

    def refresh(self):
        """Refreshes the access token"""
        print("refreshing token")
        oauth2session = OAuth2Session(
            client_id=self.client_id,
            scope=self.scope,
        )
        token_url = "https://api.kroger.com/v1/connect/oauth2/token"
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        new_token = oauth2session.refresh_token(
            token_url=token_url,
            refresh_token=self.refresh_token,
            **extra
        )

        # Update token details
        self.token = new_token['access_token']
        self.refresh_token = new_token['refresh_token']
        self.token_type = new_token['token_type']
        self.expiry = datetime.utcfromtimestamp(new_token['expires_at'])
