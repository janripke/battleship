import os
import json
from pathlib import Path
import logging
from logging.config import dictConfig
import battleship

FILE_NOT_FOUND = "File '{}' not found."


def lookup(*filename):
    """
    Return a the absolute path of the given filename, after looking in the current folder,
    .name folder located in the home folder, package folder or
    the path the filename itself points to

    :param properties
    :param filename:
    :return:
    """
    # check for the file in the current folder
    url = os.path.join(os.getcwd(), *filename)
    if os.path.isfile(url):
        return url

    # check for the file in the home folder
    url = os.path.join(str(Path.home()), '.noted', *filename)
    if os.path.isfile(url):
        return url

    # check for the file in the package folder
    url = os.path.join(os.path.dirname(battleship.__file__), *filename)
    if os.path.isfile(url):
        return url

    # check for the file in the given folder
    url = os.path.join(*filename)
    if os.path.isfile(url):
        return url

    raise FileNotFoundError(FILE_NOT_FOUND.format(str(*filename)))


def load_json(*filename):
    path = lookup(*filename)
    with open(path) as fp:
        return json.load(fp)


def load_config(username, filename):
    configurations = load_json(filename)
    return configurations.get(username)


def load_logger(filename, name=None):
    settings = load_json(filename)
    dictConfig(settings)
    if name:
        logging.root.name = name


def responsify(**kwargs):
    return kwargs