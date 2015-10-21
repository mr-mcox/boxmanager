from boxmanager.authenticate import BoxAuthenticator
from unittest.mock import MagicMock
import os


def test_store_tokens(monkeypatch):
    monkeypatch.setattr(BoxAuthenticator, 'import_config', MagicMock)
    ba = BoxAuthenticator(None)
    ba.config = {'box_access_token_file': 'at.txt',
                 'box_refresh_token_file': 'rt.txt'}
    ba.store_tokens('access', 'refresh')
    assert open(ba.config['box_access_token_file']).readline() == 'access'
    assert open(ba.config['box_refresh_token_file']).readline() == 'refresh'
    os.remove(ba.config['box_access_token_file'])
    os.remove(ba.config['box_refresh_token_file'])
