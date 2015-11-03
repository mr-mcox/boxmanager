from unittest.mock import patch, MagicMock
from boxmanager.box_wrapper import BoxFolder
import pytest
import csv
import filecmp


@pytest.fixture
def mocked_folder(monkeypatch):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    bf = BoxFolder(None, None)
    bf._box_item = MagicMock()
    return bf


@pytest.fixture
def nested_folder(monkeypatch, mocked_folder):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    fold1 = BoxFolder()
    fold1.enable_folder_upload_email = MagicMock()

    monkeypatch.setattr(BoxFolder, 'items', [fold1])
    bf = mocked_folder
    return bf


@pytest.fixture
def nested_folder_with_emails(monkeypatch):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())

    fold1 = BoxFolder()
    fold1._folder_upload_email_address = 'email1'
    setattr(fold1, 'name', 'fold1')
    fold2 = BoxFolder(parent=fold1)
    fold2._folder_upload_email_address = 'email2'
    setattr(fold2, 'name', 'fold2')

    fold1._items = [fold2]
    fold2._items = list()
    return fold1


def test_enable_folder_upload_email_folder(monkeypatch, mocked_folder):
    box_folder = mocked_folder
    box_folder._folder_upload_email_address = None
    with patch.object(BoxFolder, '_enable_single_folder_upload_email', return_value='link') as sl_mock:
        box_folder.enable_folder_upload_email()
    sl_mock.assert_called_with()


def test_enable_folder_upload_email_no_call_when_present(monkeypatch, mocked_folder):
    # We don't want the shared link reset accidentally
    box_folder = mocked_folder
    monkeypatch.setattr(BoxFolder, 'has_folder_upload_email_address', True)
    with patch.object(BoxFolder, '_enable_single_folder_upload_email') as sl_mock:
        box_folder.enable_folder_upload_email()
    sl_mock.assert_not_called()


def test_enable_folder_upload_email_nested(nested_folder):
    box_folder = nested_folder
    box_folder.enable_folder_upload_email(recursive=True)
    for item in box_folder.items:
        item.enable_folder_upload_email.assert_called_with(
            recursive=True, num=1)


def test_create_report_of_emails(tmpdir, nested_folder_with_emails):
    with open(str(tmpdir.join('expected.csv')), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['path', 'name', 'folder_upload_email_address'])
        writer.writerow(['fold1', 'fold1', 'email1'])
        writer.writerow(['fold1/fold2', 'fold2', 'email1'])
    box_folder = nested_folder_with_emails

    print(str(tmpdir))
    box_folder.folder_upload_email_address_report(rep_dir=str(tmpdir))

    expected_csv = str(tmpdir.join('expected.csv'))
    actual_csv = str(tmpdir.join('folder_upload_emails.csv'))

    assert filecmp.cmp(expected_csv, actual_csv)
