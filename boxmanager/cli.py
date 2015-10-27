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

    if args.command == 'enable_shared_link':
        client = BoxAuthenticator().box_client
        folder = BoxFolder(client, args.folder)
        folder.enable_shared_link(recursive=True)


if __name__ == '__main__':
    parse_command_line()
