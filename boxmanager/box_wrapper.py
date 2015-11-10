from boxsdk.object.folder import Folder
from boxsdk.object.file import File
import os
import csv
from datetime import datetime
import logging
import pandas as pd

def print_progress(num):
    print("Completed {} items".format(num), end='\r')


class BoxItem(object):

    """Wrapper for BoxSDK Item"""

    def __init__(self, response_object=None, parent=None):
        self.parent = parent

    def get_shared_link(self):
        logging.debug("get_shared_link")
        return self._box_item.get_shared_link()

    @property
    def item_info(self):
        if not hasattr(self, '_item_info'):
            logging.debug("item_info")
            self._item_info = self._box_item.get()
        return self._item_info

    @property
    def has_shared_link(self):
        return (self.shared_link is not None)

    def enable_shared_link(self):
        if not self.has_shared_link:
            self.shared_link = self.get_shared_link()
            assert self.has_shared_link, "Box item " + \
                self.id + " failed to enable shared link"

    @property
    def download_count(self):
        if not hasattr(self, '_download_count'):
            if self.has_shared_link:
                logging.debug("item_info for download count")
                self._download_count = self.item_info['shared_link'][
                    'download_count']
            else:
                self._download_count = None
        return self._download_count

    @property
    def preview_count(self):
        if not hasattr(self, '_preview_count'):
            if self.has_shared_link:
                logging.debug("item_info for preview count")
                self._preview_count = self.item_info['shared_link'][
                    'preview_count']
            else:
                self._preview_count = None
        return self._preview_count

    @property
    def path(self):
        if not hasattr(self, '_path'):
            if self.parent is None:
                self._path = self.name
            else:
                self._path = os.path.join(self.parent.path, self.name)
        return self._path

    def _folder_access_stats_report_info(self, parent_path, num=0):
        name = self.name
        path_to_item = os.path.join(parent_path, name)
        num = num + 1
        print_progress(num)
        return (num, [[path_to_item, name,
                       self.preview_count,
                       self.download_count]])

    def _item_attribute_records(self, headers, num=0):
        num = num + 1
        print_progress(num)
        records = list()
        for head in headers:
            if hasattr(self, head):
                records.append(getattr(self, head))
            else:
                records.append(None)
        return (num, [records])

    def nowstamp(self):
        return datetime.utcnow().strftime('%Y%m%d%H%M')

    def add_attribute(self, key, value):
        if type(value) is dict:
            for k, v in value.items():
                k_name = key + "_" + k
                self.add_attribute(k_name, v)
                self.attr_in_useful_fields(k_name)
        else:
            setattr(self, key, value)
            self.attr_in_useful_fields(key)

    def attr_in_useful_fields(self, key):
        if key not in self.all_useful_fields:
            self.all_useful_fields.append(key)


    def setup_fields(self):
        logging.debug("setup_fields")
        box_item = self._box_item
        resp_object = box_item._response_object
        if len(resp_object.keys()) == 0:
            logging.debug("setup_fields-2nd time")
            box_item = self._box_item.get(fields=self.non_dict_fields)
            resp_object = box_item._response_object
        self._item_info = resp_object
        for key in resp_object.keys():
            self.add_attribute( key, box_item[key])

    non_dict_fields = ['purged_at',
                       'sequence_id',
                       'created_at',
                       'content_created_at',
                       'trashed_at',
                       'name',
                       'modified_at',
                       'description',
                       'type',
                       'id',
                       'folder_upload_email',
                       'etag',
                       'size',
                       'item_status',
                       'content_modified_at',
                       'shared_link']
    all_useful_fields = non_dict_fields + \
        ['path', 'folder_upload_email',
            'download_count', 'preview_count']


class BoxFile(BoxItem):

    """Wrapper for BoxSDK File"""

    def __init__(self, client=None, file_id=None, item=None, parent=None):
        """File must be initated with either the client and file_id
        or an already created Box File

        :param client:
            The Box Client
        :type client:
            :class:`Client`
        :param file_id:
            Box generated id for the file
        :type file_id:
            `int`
        :param item:
            The Box item
        :type item:
            :class: `File`
        """
        super(BoxFile, self).__init__(parent=parent)
        if item is not None:
            logging.debug("BoxFile Init")
            self._box_item = item
            self.setup_fields()
        else:
            logging.debug("BoxFile Init-2nd")
            self.set_box_item(client, file_id)

    def set_box_item(self, client, file_id):
        logging.debug("File-set_box_item")
        self._box_item = client.file(file_id=file_id)
        self.setup_fields()


class BoxFolder(BoxItem):

    """Wrapper for BoxSDK Folder"""

    def __init__(self, client=None, folder_id=None, item=None, parent=None):
        """Folder must be initated with either the client and folder_id
        or an already created Box Folder

        :param client:
            The Box Client
        :type client:
            :class:`Client`
        :param folder_id:
            Box generated id for the folder
        :type folder_id:
            `int`
        :param item:
            The Box item
        :type item:
            :class: `Folder`
        """

        super(BoxFolder, self).__init__(parent=parent)

        self.item_limit = 200

        self.client = client

        if item is not None:
            logging.debug("BoxFolder Init")
            self._box_item = item
            self.setup_fields()
        else:
            logging.debug("BoxFolder Init-2nd")
            self.set_box_item(client, folder_id)

    def set_box_item(self, client, folder_id):
        logging.debug("BoxFile set_box_item")
        self._box_item = client.folder(folder_id=folder_id)
        self.setup_fields()

    @property
    def items(self):
        """Return a list of BoxFile and BoxFolder items
           that are children of this folder"""

        if not hasattr(self, '_items'):
            logging.debug("items")
            box_items = self._box_item.get_items(
                self.item_limit, fields=self.non_dict_fields)
            items = list()
            for item in box_items:
                if type(item) is File:
                    items.append(BoxFile(item=item, parent=self))
                elif type(item) is Folder:
                    items.append(BoxFolder(item=item, parent=self))
            self._items = items
        return self._items

    def upload(self, file_path, file_name):
        logging.debug("Upload")
        self._box_item.upload(file_path=file_path, file_name=file_name)

    def upload_and_remove_local(self, file_path, file_name):
        self.upload(file_path=file_path, file_name=file_name)
        os.remove(file_path)

    def enable_shared_link(self, recursive=False, num=0):
        """Enable shared link for the folder

        :param recursive:
            Whether or not to set shared link for file/folder under this one
        :type recursive:
            `bool`
        :param int num:
            The number of previously run items - used for printing progress
        """
        super(BoxFolder, self).enable_shared_link()
        if recursive:
            for item in self.items:
                if type(item) is BoxFolder:
                    num = num + 1
                    print_progress(num)
                    num = item.enable_shared_link(recursive=True,  num=num)
                else:
                    num = num + 1
                    print_progress(num)
                    item.enable_shared_link()
        return num

    @property
    def folder_upload_email_address(self):
        if not hasattr(self, '_folder_upload_email_address'):
            self._folder_upload_email_address = self._get_folder_upload_email()
        return self._folder_upload_email_address

    @property
    def has_folder_upload_email_address(self):
        return (self.folder_upload_email_address is not None)

    def _get_folder_upload_email(self):
        logging.debug("item_info for folder upload email")
        email_obj = self.item_info['folder_upload_email']
        if email_obj is not None:
            return email_obj['email']
        else:
            return None

    def _enable_single_folder_upload_email(self):
        logging.debug("_enable_single_folder_upload_email")
        self._box_item.update_info({'folder_upload_email': {'access': 'open'}})
        self._get_folder_upload_email()
        assert self.has_folder_upload_email_address, "Box item " + \
            self.id + " failed to enable shared link"

    def enable_folder_upload_email(self, recursive=False, num=0):
        """Enable folder upload email for the folder

        :param recursive:
            Whether or not to set folder upload email for file/folder under this one
        :type recursive:
            `bool`
        :param int num:
            The number of previously run items - used for printing progress
        """
        if not self.has_folder_upload_email_address:
            self._enable_single_folder_upload_email()
        if recursive:
            for item in self.items:
                if type(item) is BoxFolder:
                    num = num + 1
                    print_progress(num)
                    num = item.enable_folder_upload_email(
                        recursive=True,  num=num)
        return num

    def folder_upload_email_address_report(self, rep_dir=os.getcwd()):
        """Save a CSV formatted report of folder emails

        :param str rep_dir:
            The directory to place the report in (defaults to current directory)
        """
        report_path = str(os.path.join(rep_dir, 'folder_upload_emails.csv'))

        headers = ['path', 'name', 'folder_upload_email_address']
        (num, records) = self._item_attribute_records(headers)

        with open(report_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for row in records:
                writer.writerow(row)

    def folder_access_stats_report(self, rep_dir=os.getcwd()):
        """Save a CSV formatted report of access stats

        :param str rep_dir:
            The directory to place the report in (defaults to current directory)
        """

        report_path = str(
            os.path.join(rep_dir, self.nowstamp() + '-access_stats.csv'))

        headers = ['path', 'name', 'preview_count', 'download_count']
        (num, records) = self._item_attribute_records(headers)

        with open(report_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for row in records:
                writer.writerow(row)

    def _item_attribute_records(self, headers, num=0):
        (num, records) = super(
            BoxFolder, self)._item_attribute_records(headers, num=num)
        for item in self.items:
            (num, new_records) = item._item_attribute_records(headers, num=num)
            records = records + new_records
        return (num, records)

    def complete_report(self, rep_dir=os.getcwd(), box_folder=None):
        """Save a CSV formatted report of a variety of statistics

        :param str rep_dir:
            The directory to place the report in (defaults to current directory)
        """
        report_name = self.nowstamp() + '-' + str(self.id) + \
           '-' + self.name + '-complete_report.xlsx'
        report_path = str(os.path.join(rep_dir, report_name))

        headers = self.all_useful_fields
        (num, records) = self._item_attribute_records(headers)

        df = pd.DataFrame.from_records(records, columns=headers)
        df.to_excel(report_path, index=False)

        if box_folder is not None:
            bf = BoxFolder(client=self.client, folder_id=box_folder)
            bf.upload_and_remove_local(
                file_path=report_path, file_name=report_name)
