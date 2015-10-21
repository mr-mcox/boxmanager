from unittest.mock import patch, MagicMock
from boxmanager.box_wrapper import BoxFile
import pytest


@pytest.fixture
def mocked_file(monkeypatch):
    monkeypatch.setattr(BoxFile, 'set_box_file', MagicMock)
    bf = BoxFile(None, None)
    bf._box_file = MagicMock()
    return bf


def test_enable_shared_link_file(monkeypatch, mocked_file):
    box_file = mocked_file
    monkeypatch.setattr(BoxFile, 'has_shared_link', False)
    with patch.object(BoxFile, 'get_shared_link') as sl_mock:
        box_file.enable_shared_link()
    sl_mock.assert_called_with()


def test_enable_shared_link_no_call_when_present(monkeypatch, mocked_file):
    # We don't want the shared link reset accidentally
    box_file = mocked_file
    monkeypatch.setattr(BoxFile, 'has_shared_link', True)
    with patch.object(BoxFile, 'get_shared_link') as sl_mock:
        box_file.enable_shared_link()
    sl_mock.assert_not_called()
