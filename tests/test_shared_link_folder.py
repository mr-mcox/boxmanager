from unittest.mock import patch, MagicMock
from boxmanager.box_wrapper import BoxFolder
import pytest


@pytest.fixture
def mocked_folder(monkeypatch):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock)
    bf = BoxFolder(None, None)
    bf._box_item = MagicMock()
    return bf


def test_enable_shared_link_folder(monkeypatch, mocked_folder):
    box_folder = mocked_folder
    monkeypatch.setattr(BoxFolder, 'has_shared_link', False)
    with patch.object(BoxFolder, 'get_shared_link') as sl_mock:
        box_folder.enable_shared_link()
    sl_mock.assert_called_with()


def test_enable_shared_link_no_call_when_present(monkeypatch, mocked_folder):
    # We don't want the shared link reset accidentally
    box_folder = mocked_folder
    monkeypatch.setattr(BoxFolder, 'has_shared_link', True)
    with patch.object(BoxFolder, 'get_shared_link') as sl_mock:
        box_folder.enable_shared_link()
    sl_mock.assert_not_called()
