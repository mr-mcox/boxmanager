Readme
*******

Installation
=============
Run the following command from the Annaconda Command Prompt

*pip3 install git+https://github.com/mr-mcox/boxmanager.git@v0.4.6#egg=boxmanager*

If you've already installed it, then you'll need to run a modified version to update:

*pip3 install --upgrade git+https://github.com/mr-mcox/boxmanager.git@v0.4.6#egg=boxmanager*

Initial setup
=============
1. Sign up for a Box Developer account at https://developer.box.com
2. Create a Box Application
3. Copy the config.yaml file in this repository into the folder you want to run boxmanager from (this will likely be a new folder)
4. Set the box client id and box client secret in the config.yaml file to the values from the Box Application you just created.
5. You should now be able to follow instructions in the Set Up Folder For Running Box Manager at https://docs.google.com/document/d/1rAQHAlMB4d10K2Cb_rsJfKuiJJYmo2FY7Xbeu_elYB8/edit#heading=h.p2i5ksomg3bq

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
