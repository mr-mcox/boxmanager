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

    def enable_shared_link(self):
        self.get_shared_link()
