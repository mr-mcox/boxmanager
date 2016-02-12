Readme
*******

Installation
=============
Run the following command from the Annaconda Command Prompt

*pip3 install git+https://github.com/mr-mcox/boxmanager.git@v0.4.5#egg=boxmanager*

If you've already installed it, then you'll need to run a modified version to update:

*pip3 install --upgrade git+https://github.com/mr-mcox/boxmanager.git@v0.4.5#egg=boxmanager*

Initial setup
=============
You will need a special config file that has some secret information. Contact Matthew to get this.

Usage
======
Here are sample commands you can run. Each of these must be run from the folder with the config file.

*python -m boxmanager.cli enable_shared_link BOXFOLDERID*

*python -m boxmanager.cli enable_folder_upload_email BOXFOLDERID*

*python -m boxmanager.cli folder_upload_email_report BOXFOLDERID*

*python -m boxmanager.cli folder_access_stats_report BOXFOLDERID*

*python -m boxmanager.cli complete_report BOXFOLDERID*

*python -m boxmanager.cli complete_report BOXFOLDERID -d OUTPUT_DIRECTORY*

Substitute BOXFOLDERID with the integer ID for the root folder you are running the command for