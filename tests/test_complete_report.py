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


def test_complete_report(monkeypatch,
                         tmpdir,
                         nested_folder_with_various_stats):
    def nowstamp(self):
        return datetime(2015, 10, 30, 20, 20, 38).strftime('%Y%m%d%H%M')

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
    box_folder = nested_folder_with_various_stats

    box_folder.complete_report(rep_dir=str(tmpdir))

    expected_csv = str(tmpdir.join('expected.csv'))
    actual_csv = str(
        tmpdir.join(nowstamp(None) + '-' + str(fold1.id) + '-complete_report.csv'))

    assert filecmp.cmp(expected_csv, actual_csv)
