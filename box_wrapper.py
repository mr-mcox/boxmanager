from boxsdk.object.file import File
from boxsdk.object.folder import Folder


class BoxFile(File):

    """Wrapper for BoxSDK File"""

    def __init__(self, client, file_id):
        self.set_box_file(client, file_id)

    def set_box_file(self, client, file_id):
        self._box_file = client.file(file_id=file_id)

    def get_shared_link(self):
        return self._box_file.get_shared_link()

    @property
    def shared_link(self):
        if not hasattr(self, '_shared_link'):
            self._shared_link = self._box_file.get('shared_link')
        return self._shared_link

    @property
    def has_shared_link(self):
        return self._shared_link is not None

    def enable_shared_link(self):
        if not self.has_shared_link:
            self._shared_link = self.get_shared_link()
