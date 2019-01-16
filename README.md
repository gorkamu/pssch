# 🤐🤐 Pssch

This is a proof of concept of a multiplatform python keylogger.
This script runs on windows as well as mac osx and linux.

Things that already do:
- Multiplatform support
- Key events detection
- I/O control to manage the creation and delete of the log file
- Log Sending via Gmail Mehtod
- Ability to be self added to the Windows Registry (regedit)

Things that work halfway:
- Docker support
- Windows run on startup

To enable the email sending via gmail just activate the following option [https://myaccount.google.com/lesssecureapps?pli=1](https://myaccount.google.com/lesssecureapps?pli=1)

## How to install
First of all install dependencies
``` bash
    pip install -r ./requirements.txt
```
If this method throws you an error, launch the following commands:
``` bash
    pip install pynput
    pip install keyboard
```

After that, you have to configure the script's properties such as LOG_FILE or GMAIL_ACCOUNT.
To do that just edit the pssch.py file and modifity the following properties;

``` bash
    self.EMAIL_FROM='pssch@gmail.com'
    self.EMAIL_TO='blablabla@gmail.com'
    self.GMAIL_USER='bliblibli@gmail.com'
    self.GMAIL_PWD='****'
    self.LOG_FILE = '/Users/blabla/log.dat'
```

Fill them before start the script

To launch and run the script:
``` bash
    python pssch.py
```

if during the execution the script fails due to lack of parameters you will see something like the following

![Pssch Keylogger Error](https://i.imgur.com/7DQQgwB.png)

## Development resources
- https://www.programcreek.com/python/example/95388/pynput.keyboard.Listener
- https://theembeddedlab.com/tutorials/keylogger-python/
- https://nitratine.net/blog/post/python-keylogger/?utm_source=pythonanywhere&utm_medium=redirect&utm_campaign=pythonanywhere_organic_redirect#it-doesnt-work-general-things-to-try
- https://github.com/ajinabraham/Xenotix-Python-Keylogger/blob/master/xenotix_python_logger.py
