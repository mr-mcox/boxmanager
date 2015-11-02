from unittest.mock import patch, MagicMock
from boxmanager.box_wrapper import BoxFolder, BoxFile, BoxItem
import pytest
import csv
import filecmp
from datetime import datetime

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


@pytest.fixture
def nested_folder(monkeypatch, mocked_folder):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    fold1 = BoxFolder()
    fold1.enable_shared_link = MagicMock()

    monkeypatch.setattr(BoxFolder, 'items', [fold1])
    bf = mocked_folder
    return bf


@pytest.fixture
def nested_folder_with_access_stats(monkeypatch):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    monkeypatch.setattr(BoxFile, 'set_box_item', MagicMock())
    monkeypatch.setattr(BoxItem, 'has_shared_link', True)

    fold1 = BoxFolder()
    fold1._download_count = 1
    fold1._preview_count = 2
    setattr(fold1, 'name', 'fold1')
    fold2 = BoxFolder()
    fold2._download_count = 2
    fold2._preview_count = 3
    setattr(fold2, 'name', 'fold2')
    file1 = BoxFile()
    file1._download_count = 5
    file1._preview_count = 6
    file1._name = 'file1'
    setattr(file1, 'name', 'file1')
    fold1._items = [fold2]
    fold2._items = [file1]
    return fold1


def test_enable_shared_link_folder(monkeypatch, mocked_folder):
    box_folder = mocked_folder
    box_folder._shared_link = None
    with patch.object(BoxFolder, 'get_shared_link', return_value='link') as sl_mock:
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


def test_enable_shared_link_nested(monkeypatch,
                                   nested_folder):
    box_folder = nested_folder
    box_folder.enable_shared_link(recursive=True)
    for item in box_folder.items:
        item.enable_shared_link.assert_called_with(recursive=True, num=1)


def test_create_report_of_access_stats(monkeypatch,
                                       tmpdir,
                                       nested_folder_with_access_stats):
    def nowstamp(self):
        return datetime(2015, 10, 30, 20, 20, 38).strftime('%Y%m%d%H%M')

    monkeypatch.setattr(BoxItem, 'nowstamp', nowstamp)
    with open(str(tmpdir.join('expected.csv')), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['path', 'name', 'preview_count', 'download_count'])
        writer.writerow(['fold1', 'fold1', 2, 1])
        writer.writerow(['fold1/fold2', 'fold2', 3, 2])
        writer.writerow(['fold1/fold2/file1', 'file1', 6, 5])
    box_folder = nested_folder_with_access_stats

    box_folder.folder_access_stats_report(rep_dir=str(tmpdir))

    expected_csv = str(tmpdir.join('expected.csv'))
    actual_csv = str(
        tmpdir.join(nowstamp(None) + '-access_stats.csv'))

    assert filecmp.cmp(expected_csv, actual_csv)
