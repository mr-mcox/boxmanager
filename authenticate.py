from boxsdk import OAuth2, Client
import os
import yaml
import sys


class BoxAuthenticator(object):

    """CLient for connecting to Box"""

    def __init__(self, config_file):
        self.import_config(config_file)

    def import_config(self, config_file):
        self.config = yaml.load(open(config_file))

    def store_tokens(self, access_token, refresh_token):
        """
        Store tokens in local file when they are modified
        Assumes that the following are present in the config file
        box_access_token_file
        box_refresh_token_file
        """

        at = open(self.config['box_access_token_file'], 'w')
        rt = open(self.config['box_refresh_token_file'], 'w')
        at.write(access_token)
        rt.write(refresh_token)
        at.close()
        rt.close()

    def authenticate_client(self):
        """Return client
        Assumes that the following are present in the config file
        box_access_token_file
        box_refresh_token_file
        box_client_id
        box_client_secret
        :return: Box Client
        """
        access_token_present = os.path.isfile(
            self.config['box_access_token_file'])
        refresh_token_present = os.path.isfile(
            self.config['box_refresh_token_file'])

        access_token = None
        refresh_token = None
        oauth = None
        if access_token_present and refresh_token_present:
            at = open(self.config['box_access_token_file'])
            access_token = at.readline()
            rt = open(self.config['box_refresh_token_file'])
            refresh_token = rt.readline()

            oauth = OAuth2(
                client_id=self.config['box_client_id'],
                client_secret=self.config['box_client_secret'],
                access_token=access_token,
                refresh_token=refresh_token,
                store_tokens=self.store_tokens)
            oauth.refresh(oauth.access_token)
        else:
            oauth = OAuth2(
                client_id=self.config['box_client_id'],
                client_secret=self.config['box_client_secret'],
                store_tokens=self.store_tokens,
            )
            auth_url, csrf_token = oauth.get_authorization_url(
                'http://localhost')
            print("Please go to " + auth_url + " to authenticate")
            auth_code = input('Authorization Code: ')
            access_token, refresh_token = oauth.authenticate(auth_code)

        return Client(oauth)

    @property
    def box_client(self):
        if not hasattr(self, '_box_client'):
            self._box_client = self.authenticate_client()
        return self._box_client


if __name__ == '__main__':
    BoxAuthenticator(sys.argv[1]).box_client