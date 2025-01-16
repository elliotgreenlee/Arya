import webbrowser
import wsgiref.simple_server
import wsgiref.util
from Utils.utils import load_json
from KrogerCredentials import KrogerCredentials
from requests_oauthlib import OAuth2Session
from datetime import datetime


class KrogerFlow:
    def __init__(self, oauth2session, client_config):

        if client_config['client_type'] == "installed" or client_config['client_type'] == "web":
            self.client_type = client_config['client_type']
        else:
            raise ValueError("Client secrets must be for a web or installed app.")

        self.client_config = client_config
        self.oauth2session = oauth2session
        self.redirect_uri = client_config['redirect_uri']

    @classmethod
    def from_client_secrets_file(cls, client_secrets_file, scope):
        """
        Create a KrogerFlow instance (Installed or Web) with an OAuth2Session
        from a Kroger client secrets file. This will then run either
        the Installed app or Web app flow.
        """

        client_config = load_json(client_secrets_file)

        if scope:
            client_config['scope'] = scope

        oauth2session = OAuth2Session(client_id=client_config["client_id"],
                                      scope=client_config["scope"],
                                      redirect_uri=client_config['redirect_uri'])

        return cls(
            oauth2session,
            client_config,
        )

    def authorization_url(self):
        """First step of flow, generates an authorization URL with details from the session"""

        auth_uri = "https://api.kroger.com/v1/connect/oauth2/authorize"
        url, _ = self.oauth2session.authorization_url(auth_uri)

        return url

    def fetch_token(self, authorization_response):
        """Completes the Authorization Flow and obtains an access token after user consents."""

        return self.oauth2session.fetch_token("https://api.kroger.com/v1/connect/oauth2/token",
                                              client_secret=self.client_config['client_secret'],
                                              authorization_response=authorization_response)

    @property
    def credentials(self):
        """Must call fetch_token before use"""
        if not self.oauth2session.token:
            raise ValueError("There is no token for this session, did you call " "fetch_token?")

        credentials = KrogerCredentials(
            self.client_config['client_id'],
            self.client_config['client_secret'],
            self.client_config['scope'],
            token=self.oauth2session.token['access_token'],
            refresh_token=self.oauth2session.token['refresh_token'],
            token_type=self.oauth2session.token['token_type'],
            expiry=datetime.utcfromtimestamp(self.oauth2session.token["expires_at"]))

        return credentials

    def authorized_session(self):
        """
        # Example of making a request using the session
        response = session.get("https://api.example.com/protected-resource")
        """
        # TODO: something with self.credentials, not critical right now
        session = OAuth2Session(self.credentials)

        return session


class InstalledAppFlow(KrogerFlow):
    """Authorization flow helper for installed applications."""

    def run_local_server(self, host="localhost", port=8081,
                         bind_addr=None, open_browser=True):
        """Run the flow using the server strategy.

        The server strategy instructs the user to open the authorization URL in
        their browser and will attempt to automatically open the URL for them.
        It will start a local web server to listen for the authorization
        response. Once authorization is complete the authorization server will
        redirect the user's browser to the local web server. The web server
        will get the authorization code from the response and shutdown. The
        code is then exchanged for a token.

        Args:
            host (str): The hostname for the local redirect server. This will
                be served over http, not https.
            bind_addr (str): Optionally provide an ip address for the redirect
                server to listen on when it is not the same as host
                (e.g. in a container). Default value is None,
                which means that the redirect server will listen
                on the ip address specified in the host parameter.
            port (int): The port for the local redirect server.
            open_browser (bool): Whether or not to open the authorization URL
                in the user's browser.
        """
        wsgi_app = RedirectWSGIApp("The authentication flow has completed. You may close this window.")
        # Fail fast if the address is occupied
        wsgiref.simple_server.WSGIServer.allow_reuse_address = False
        local_server = wsgiref.simple_server.make_server(
            bind_addr or host, port, wsgi_app, handler_class=wsgiref.simple_server.WSGIRequestHandler
        )

        try:
            self.redirect_uri = "http://{}:{}/callback".format(host, local_server.server_port)
            auth_url = self.authorization_url()

            if open_browser:
                # if browser is None it defaults to default browser
                webbrowser.get(None).open(auth_url, new=1, autoraise=True)
            print("Please visit this URL to authorize this application: {url}".format(url=auth_url))

            local_server.handle_request()

            # OAuth 2.0 should only occur over https.
            authorization_response = wsgi_app.last_request_uri.replace("http", "https")
            self.fetch_token(authorization_response=authorization_response)
        finally:
            local_server.server_close()

        return self.credentials


class RedirectWSGIApp(object):
    """WSGI app to handle the authorization redirect.
    https://docs.python.org/3/library/wsgiref.html#module-wsgiref.simple_server
    Stores the request URI and displays the given success message.
    """

    def __init__(self, success_message):
        """
        Args:
            success_message (str): The message to display in the web browser
                the authorization flow is complete.
        """
        self.last_request_uri = None
        self._success_message = success_message

    def __call__(self, environ, start_response):
        """WSGI Callable.

        Args:
            environ (Mapping[str, Any]): The WSGI environment.
            start_response (Callable[str, list]): The WSGI start_response
                callable.

        Returns:
            Iterable[bytes]: The response body.
        """
        start_response("200 OK", [("Content-type", "text/plain; charset=utf-8")])
        self.last_request_uri = wsgiref.util.request_uri(environ)
        return [self._success_message.encode("utf-8")]


