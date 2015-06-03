# coding: utf8

# PASSWORD READER
# author: Karel Jilek
#
# Script to retrieve passwords from the 'passwords.pwd' file.
#
# USAGE:
# password = Password().read("password_description")
# for example: "SafeQ"
#
# PASSWORDS.PWD SYNTAX:
# my_very_secret_password   #password_description
# for example: baka123   #bakalari
#
# DO NOT WRITE ANY PASSWORDS BELOW THE "EOF" LINE, all the lines below are ignored

from os.path import dirname

class Password:

    def __init__(self):

        self.pwds = {}

        try:
            f = open(dirname(__file__) + '/../passwords.pwd')
        except IOError:
            raise Exception("File 'passwords.pwd' not found")

        for line in f:
            try:
                if line.rstrip() == "EOF":
                    break
                x = line.split("#")
                self.pwds[x[1].rstrip()] = x[0].rstrip()
            except:
                raise Exception("File 'passwords.pwd' is corrupted")

    def read(self, pwd):

        if not pwd in self.pwds.keys():
            raise Exception("Cannot find reference of '"+pwd+"' password in 'passwords.pwd'")

        return self.pwds[pwd]