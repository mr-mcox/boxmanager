import argparse
from boxmanager.box_wrapper import BoxFolder
from boxmanager.authenticate import BoxAuthenticator


def parse_command_line(cli_input=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command to execute",
                        type=str)
    parser.add_argument(
        "-f", "--folder", action='store', help="id of folder to use")
    args = None
    if cli_input is not None:
        args = parser.parse_args(cli_input)
    else:
        args = parser.parse_args()

    command_handled = False

    client = BoxAuthenticator().box_client

    if args.command == 'enable_shared_link':
        folder = BoxFolder(client, args.folder)
        folder.enable_shared_link(recursive=True)
        command_handled = True

    if args.command == 'enable_folder_upload_email':
        folder = BoxFolder(client, args.folder)
        folder.enable_folder_upload_email(recursive=True)
        command_handled = True

    if args.command == 'folder_upload_email_report':
        folder = BoxFolder(client, args.folder)
        folder.folder_upload_email_report()
        command_handled = True

    if args.command == 'folder_access_stats_report':
        folder = BoxFolder(client, args.folder)
        folder.folder_access_stats_report()
        command_handled = True

    assert command_handled, "Command not recognized " + args.command

if __name__ == '__main__':
    parse_command_line()
