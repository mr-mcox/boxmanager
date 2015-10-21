from unittest.mock import patch, MagicMock
import pytest
import boxmanager
from boxmanager.box_wrapper import BoxFile
from boxsdk.object.file import File
from boxsdk.object.folder import Folder


@pytest.fixture
def mocked_file(monkeypatch):
    monkeypatch.setattr(BoxFile,'set_box_file', MagicMock)
    bf = BoxFile(None, None)
    bf._box_file = MagicMock()
    return bf


def test_enable_shared_link_file(mocked_file):
    box_file = mocked_file
    with patch.object(BoxFile, 'get_shared_link') as sl_mock:
        box_file.enable_shared_link()
    sl_mock.assert_called_with()
