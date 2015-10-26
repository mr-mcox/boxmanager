from unittest.mock import MagicMock
from boxmanager.box_wrapper import BoxFolder
from boxmanager.authenticate import BoxAuthenticator
from boxmanager.cli import parse_command_line


def test_call_shared_links(monkeypatch):
    enable_shared_link_mock = MagicMock()
    set_box_item_mock = MagicMock()
    monkeypatch.setattr(
        BoxFolder, 'enable_shared_link', enable_shared_link_mock)
    monkeypatch.setattr(BoxFolder, 'set_box_item', set_box_item_mock)
    monkeypatch.setattr(BoxAuthenticator, 'box_client', 'the_client')

    parse_command_line(['enable_shared_link', '-f', '1234'])
    set_box_item_mock.assert_called_with('the_client', '1234')
    enable_shared_link_mock.assert_called_with(recursive=True)
