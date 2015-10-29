from boxsdk.object.folder import Folder
from boxsdk.object.file import File
import os
import csv


def print_progress(num):
    print("Completed {} items".format(num), end='\r')


class BoxItem(object):

    """Wrapper for BoxSDK Item"""

    def __init__(self):
        pass

    def get_shared_link(self):
        return self._box_item.get_shared_link()

    @property
    def item_info(self):
        if not hasattr(self, '_item_info'):
            self._item_info = self._box_item.get()
        return self._item_info

    @property
    def id(self):
        if not hasattr(self, '_id'):
            self._id = self.item_info['id']
        return self._id

    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = self.item_info['name']
        return self._name

    @property
    def shared_link(self):
        if not hasattr(self, '_shared_link'):
            self._shared_link = self.item_info['shared_link']
        return self._shared_link

    @property
    def has_shared_link(self):
        return (self.shared_link is not None)

    def enable_shared_link(self):
        if not self.has_shared_link:
            self._shared_link = self.get_shared_link()
            assert self.has_shared_link, "Box item " + \
                self.id + " failed to enable shared link"

    @property
    def download_count(self):
        if not hasattr(self, '_download_count'):
            if self.has_shared_link:
                self._download_count = self.item_info['shared_link'][
                    'download_count']
            else:
                self._download_count = None
        return self._download_count

    @property
    def preview_count(self):
        if not hasattr(self, '_preview_count'):
            if self.has_shared_link:
                self._preview_count = self.item_info['shared_link'][
                    'preview_count']
            else:
                self._preview_count = None
        return self._preview_count

    def _folder_access_stats_report_info(self, parent_path, num=0):
        name = self.name
        path_to_item = os.path.join(parent_path, name)
        return [[path_to_item, name, self.preview_count, self.download_count]]


class BoxFile(BoxItem):

    """Wrapper for BoxSDK File"""

    def __init__(self, client=None, file_id=None, item=None):
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
        super(BoxFile, self).__init__()
        if item is not None:
            self._box_item = item
        else:
            self.set_box_item(client, file_id)

    def set_box_item(self, client, file_id):
        self._box_item = client.file(file_id=file_id)


class BoxFolder(BoxItem):

    """Wrapper for BoxSDK Folder"""

    def __init__(self, client=None, folder_id=None, item=None):
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

        super(BoxFolder, self).__init__()

        self.item_limit = 200

        if item is not None:
            self._box_item = item
        else:
            self.set_box_item(client, folder_id)

    def set_box_item(self, client, folder_id):
        self._box_item = client.folder(folder_id=folder_id)

    @property
    def items(self):
        """Return a list of BoxFile and BoxFolder items
           that are children of this folder"""

        if not hasattr(self, '_items'):
            box_items = self._box_item.get_items(self.item_limit)
            items = list()
            for item in box_items:
                if type(item) is File:
                    items.append(BoxFile(item=item))
                elif type(item) is Folder:
                    items.append(BoxFolder(item=item))
                else:
                    assert False, "Item is neither File nor Folder: " + \
                        str(box_items)
            self._items = items
        return self._items

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
    def folder_upload_email(self):
        if not hasattr(self, '_folder_upload_email'):
            self._folder_upload_email = self._get_folder_upload_email()
        return self._folder_upload_email

    @property
    def has_folder_upload_email(self):
        return (self.folder_upload_email is not None)

    def _get_folder_upload_email(self):
        email_obj = self.item_info['folder_upload_email']
        if email_obj is not None:
            return email_obj['email']
        else:
            return None

    def _enable_single_folder_upload_email(self):
        self._box_item.update_info({'folder_upload_email': {'access': 'open'}})
        self._get_folder_upload_email()
        assert self.has_folder_upload_email, "Box item " + \
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
        if not self.has_folder_upload_email:
            self._enable_single_folder_upload_email()
        if recursive:
            for item in self.items:
                if type(item) is BoxFolder:
                    num = num + 1
                    print_progress(num)
                    num = item.enable_folder_upload_email(
                        recursive=True,  num=num)
        return num

    def folder_upload_email_report(self, rep_dir=os.getcwd()):
        """Save a CSV formatted report of folder emails

        :param str rep_dir:
            The directory to place the report in (defaults to current directory)
        """
        report_path = str(os.path.join(rep_dir, 'folder_upload_emails.csv'))

        records = self._folder_report_info('')

        with open(report_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['path', 'name', 'email'])
            for row in records:
                writer.writerow(row)

    def _folder_report_info(self, parent_path, num=0):
        name = self.name
        path_to_folder = os.path.join(parent_path, name)
        records = [[path_to_folder, name, self.folder_upload_email]]
        for item in self.items:
            if type(item) is BoxFolder:
                num = num + 1
                print_progress(num)
                new_records = item._folder_report_info(path_to_folder, num)
                records = records + new_records
        return records

    def folder_access_stats_report(self, rep_dir=os.getcwd()):
        """Save a CSV formatted report of access stats

        :param str rep_dir:
            The directory to place the report in (defaults to current directory)
        """
        report_path = str(os.path.join(rep_dir, 'access_stats.csv'))

        records = self._folder_access_stats_report_info('')

        with open(report_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ['path', 'name', 'preview_count', 'download_count'])
            for row in records:
                writer.writerow(row)

    def _folder_access_stats_report_info(self, parent_path, num=0):
        name = self.name
        path_to_item = os.path.join(parent_path, name)
        records = super(
            BoxFolder, self)._folder_access_stats_report_info(parent_path,
                                                              num=0)

        for item in self.items:
            num = num + 1
            print_progress(num)
            new_records = item._folder_access_stats_report_info(
                path_to_item, num=num)
            records = records + new_records
        return records
