# PyKey

This is a proof of concept of a multiplatform python keylogger

To enable the email sending via gmail just activate the following option [https://myaccount.google.com/lesssecureapps?pli=1](https://myaccount.google.com/lesssecureapps?pli=1)

## Setup
First of all install dependencies
``` bash
    pip install -r ./requirements.txt
```
On the initializing method of the PyKey class exists some properties to define the email account and other data.
Fill them before start the script
``` bash
    self.EMAIL_FROM='pykey@gmail.com'
    self.EMAIL_TO='blablabla@gmail.com'
    self.GMAIL_USER='bliblibli@gmail.com'
    self.GMAIL_PWD='****'
    self.LOG_FILE = '/Users/blabla/log.dat'
```
## How to install
If you are going to install it on Windows, first you have to install the dependencies:
``` bash
    pip install -r ./requirements.txt
```
or
``` bash
    pip install keyboard
```

Then you can launch it with the following command
``` bash
    python pykey.py
```

## Development resources
- https://www.programcreek.com/python/example/95388/pynput.keyboard.Listener
- https://theembeddedlab.com/tutorials/keylogger-python/
- https://nitratine.net/blog/post/python-keylogger/?utm_source=pythonanywhere&utm_medium=redirect&utm_campaign=pythonanywhere_organic_redirect#it-doesnt-work-general-things-to-try
- https://github.com/ajinabraham/Xenotix-Python-Keylogger/blob/master/xenotix_python_logger.py
