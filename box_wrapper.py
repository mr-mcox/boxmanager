from boxsdk.object.folder import Folder
from boxsdk.object.file import File


class BoxItem(object):

    """Wrapper for BoxSDK Item"""

    def __init__(self):
        pass

    def get_shared_link(self):
        return self._box_item.get_shared_link()

    @property
    def shared_link(self):
        if not hasattr(self, '_shared_link'):
            self._shared_link = self._box_item.get()['shared_link']
        return self._shared_link

    @property
    def has_shared_link(self):
        return (self.shared_link is not None)

    def enable_shared_link(self):
        if not self.has_shared_link:
            self._shared_link = self.get_shared_link()


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

        self.item_limit = 100

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

        if not hasattr('self', '_items'):
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

    def enable_shared_link(self, recursive=False):
        """Enable shared link for the folder

        :param recursive:
            Whether or not to set shared link for file/folder under this one
        :type recursive:
            `bool`
        """
        super(BoxFolder, self).enable_shared_link()
        if recursive:
            for item in self.items:
                if type(item) is BoxFolder:
                    item.enable_shared_link(recursive=True)
                else:
                    item.enable_shared_link()
