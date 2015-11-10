from unittest.mock import MagicMock
from boxmanager.box_wrapper import BoxFolder, BoxFile, BoxItem
import pytest


@pytest.fixture
def nested_file(monkeypatch):
    monkeypatch.setattr(BoxFolder, 'set_box_item', MagicMock())
    monkeypatch.setattr(BoxFile, 'set_box_item', MagicMock())

    fold1 = BoxFolder()
    fold1.name = 'fold1'
    fold2 = BoxFolder(parent=fold1)
    fold2.name = 'fold2'
    file1 = BoxFile(parent=fold2)
    file1.name = 'file1'
    fold1._items = [fold2]
    fold2._items = [file1]
    return file1


def test_path(nested_file):
    assert nested_file.path == 'fold1/fold2/file1'


def test_set_attr_basic(monkeypatch):
    item = BoxItem()
    item.add_attribute('key', 'value')

    assert hasattr(item, 'key')
    assert getattr(item, 'key') == 'value'


def test_set_attr_dict(monkeypatch):
    item = BoxItem()
    value = {'key2': 'value2'}
    item.add_attribute('key', value)

    assert hasattr(item, 'key_key2')
    assert getattr(item, 'key_key2') == 'value2'
    assert 'key_key2' in item.all_useful_fields
