#!/usr/bin/env python3

from api.configurator import Config
import sqlite3, os

if __name__ == '__main__':
    config = Config()
    if (config['database'].get('provider') == 'sqlite' and
            config['database'].get('file') != None):
        con = sqlite3.connect(config['database'].get('file'))
        for line in con.iterdump():
            print(line)
