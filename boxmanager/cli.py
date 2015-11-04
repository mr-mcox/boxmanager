import argparse
from boxmanager.box_wrapper import BoxFolder
from boxmanager.authenticate import BoxAuthenticator
import re


def parse_command_line(cli_input=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command to execute",
                        type=str)
    parser.add_argument("box_id", help="id of box object to use",
                        type=int)
    parser.add_argument('-d', "--directory", help="directory for outputs",
                        type=str, action='store')
    args = None
    if cli_input is not None:
        args = parser.parse_args(cli_input)
    else:
        args = parser.parse_args()

    command_handled = False

    client = BoxAuthenticator().box_client

    if args.command == 'enable_shared_link':
        folder = BoxFolder(client, args.box_id)
        folder.enable_shared_link(recursive=True)
        command_handled = True

    if args.command == 'enable_folder_upload_email':
        folder = BoxFolder(client, args.box_id)
        folder.enable_folder_upload_email(recursive=True)
        command_handled = True

    if args.command == 'folder_upload_email_address_report':
        folder = BoxFolder(client, args.box_id)
        folder.folder_upload_email_address_report()
        command_handled = True

    if args.command == 'folder_access_stats_report':
        folder = BoxFolder(client, args.box_id)
        folder.folder_access_stats_report()
        command_handled = True

    if args.command == 'complete_report':
        folder = BoxFolder(client, args.box_id)
        if args.directory is not None:
            if re.search('^\d+$', args.directory):
                folder.complete_report(box_folder=int(args.directory))
            else:
                folder.complete_report(rep_dir=args.directory)
        else:
            folder.complete_report()
        command_handled = True

    assert command_handled, "Command not recognized " + args.command

if __name__ == '__main__':
    parse_command_line()
