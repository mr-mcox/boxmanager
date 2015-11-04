from unittest.mock import patch, MagicMock
from boxmanager.box_wrapper import BoxFolder, BoxFile, BoxItem
import pytest
import csv
import filecmp
from datetime import datetime


@pytest.fixture
def nested_folder_with_various_stats(monkeypatch):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    monkeypatch.setattr(BoxFile, 'set_box_item', MagicMock())
    monkeypatch.setattr(BoxItem, 'has_shared_link', True)

    fold1 = BoxFolder()
    fold1.id = 42
    fold1._download_count = 1
    fold1._preview_count = 2
    fold1.description = 'A folder with stuff in it'
    setattr(fold1, 'name', 'fold1')
    fold2 = BoxFolder(parent=fold1)
    fold2._download_count = 2
    fold2._preview_count = 3
    setattr(fold2, 'name', 'fold2')
    file1 = BoxFile(parent=fold2)
    file1._download_count = 5
    file1._preview_count = 6
    file1._name = 'file1'
    setattr(file1, 'name', 'file1')
    fold1._items = [fold2]
    fold2._items = [file1]
    return fold1

@pytest.fixture
def nowstamp():
    return lambda x: datetime(2015, 10, 30, 20, 20, 38).strftime('%Y%m%d%H%M')

@pytest.fixture
def expected_csv(monkeypatch, tmpdir, nowstamp, nested_folder_with_various_stats):

    monkeypatch.setattr(BoxItem, 'nowstamp', nowstamp)
    header = BoxItem().all_useful_fields
    fold1 = nested_folder_with_various_stats
    fold2 = fold1._items[0]
    file1 = fold2._items[0]

    with open(str(tmpdir.join('expected.csv')), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for item in [fold1, fold2, file1]:
            row = list()
            for head in header:
                if hasattr(item, head):
                    row.append(getattr(item, head))
                else:
                    row.append(None)
            writer.writerow(row)
    

    return str(tmpdir.join('expected.csv'))


def test_complete_report(monkeypatch,
                         tmpdir,
                         nested_folder_with_various_stats, nowstamp, expected_csv):

    box_folder = nested_folder_with_various_stats
    box_folder.complete_report(rep_dir=str(tmpdir))
    fold1 = nested_folder_with_various_stats

    actual_csv = str(
        tmpdir.join(nowstamp(None) + '-' + str(fold1.id) + '-complete_report.csv'))

    assert filecmp.cmp(expected_csv, actual_csv)

def test_complete_report_and_upload(monkeypatch,
                         tmpdir,
                         nested_folder_with_various_stats, nowstamp, expected_csv):

    box_folder = nested_folder_with_various_stats

    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    upload_mock = MagicMock()
    monkeypatch.setattr(BoxFolder, 'upload_and_remove_local', upload_mock)
    box_folder.complete_report(rep_dir=str(tmpdir), box_folder=1234)

    fold1 = nested_folder_with_various_stats
    actual_csv_name = nowstamp(None) + '-' + str(fold1.id) + '-complete_report.csv'
    actual_csv_path = str(tmpdir.join(actual_csv_name))

    upload_mock.assert_called_with(file_path=actual_csv_path, file_name=actual_csv_name )