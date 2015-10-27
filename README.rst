Readme
*******

Installation
=============
Run the following command from the Annaconda Command Prompt

*pip3 install git+https://github.com/mr-mcox/boxmanager.git@master#egg=boxmanager*

Initial setup
=============
You will need a special config file that has some secret information. Contact Matthew to get this.

Usage
======
The only command at the moment is to create shared links. Run this command from the folder that has the config file:

*python -m boxmanager.cli enable_shared_link -f BOXFOLDERID*

Substitute BOXFOLDERID with the integer ID for the root folder you want to create shared links for