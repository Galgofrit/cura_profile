#!/usr/bin/python

import datetime
import os
import os.path
import platform
import re
import shutil
import sys

IGNORE = [r'.*.git/.*', r'.*\.sw.', r'.*\.pyc', r'.*\.py']

CURA_VERSION = '4.0'
if platform.system() == 'Darwin':
    CURA_CONFIG_PATH = os.path.join(r'~/Library/Application Support/cura', CURA_VERSION)
elif platform.system() == 'Windows':
    CURA_CONFIG_PATH = os.path.join(r'C:\Users\Gal\AppData\Roaming\cura', CURA_VERSION)

BACKUP_PATH = 'backup'


def recursive_ls(path):
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(path) for f in fn]


def filter_directory(directory_contents):
    filtered_contents = directory_contents[:]

    for ignored in IGNORE:
        for item in directory_contents:
            matches = re.findall(ignored, item)
            for match in matches:
                try:
                    filtered_contents.remove(match)
                except:
                    pass

    return filtered_contents


def main():
    '''
    Symlink all files in the current directory (IGNORE excluded) to Cura's
    configuration folder. Before overwriting anything, original files are backed
    up to backup/{time}/{filename}.
    '''

    backup_time = '{date:%Y-%m-%d %H:%M:%S}'.format( date=datetime.datetime.now() )

    try:
        os.makedirs(os.path.join(BACKUP_PATH, backup_time))
    except:
        pass

    to_replace = filter_directory(os.listdir('.'))

    for file_to_replace in to_replace:
        file_cura_file = os.path.join(CURA_CONFIG_PATH, file_to_replace)
        if os.path.isfile(file_cura_file):
            print 'Backing up {filename}...'.format(filename=file_to_replace)
            shutil.copy(file_cura_file, os.path.join(BACKUP_PATH, file_cura_file))

        print 'Pointing symlink{curafile} to {localfile}.'.format(
            curafile=file_cura_file, localfile=file_to_replace
        )
        os.symlink(file_to_replace, file_cura_file)

    return 0


if __name__ == '__main__':
    sys.exit(main())
