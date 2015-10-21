from unittest.mock import patch, MagicMock
from boxmanager.box_wrapper import BoxFolder
from boxmanager.box_wrapper import BoxFile
import pytest


@pytest.fixture
def mocked_folder(monkeypatch):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    bf = BoxFolder(None, None)
    bf._box_item = MagicMock()
    return bf


@pytest.fixture
def folder_with_files(monkeypatch, mocked_folder):
    monkeypatch.setattr(BoxFile, 'set_box_item', MagicMock())
    monkeypatch.setattr(BoxFile, 'enable_shared_link', MagicMock())
    f1 = BoxFile(None, None)
    f2 = BoxFile(None, None)

    monkeypatch.setattr(BoxFolder, 'items', [f1, f2])
    bf = mocked_folder
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


def test_enable_shared_link_recursive_only_file(monkeypatch,
                                                folder_with_files):
    box_folder = folder_with_files
    box_folder.enable_shared_link(recursive=True)
    for item in box_folder.items:
        item.enable_shared_link.assert_called_with()
