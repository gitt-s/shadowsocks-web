# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import sys
import os
import random
import hmac
import json
import hashlib
from colorama import Fore, Back, Style


def hmacstr(key, msg, hashtype='sha256'):
    """
    Returns HMAC string in specified hash type. Or raise NotImplementedError on
    wrong type.

    The hash type chould be one of MD5, SHA224, SHA256 and SHA512.

    By default, the hash type is SHA256.
    """
    if hashtype.lower() == 'md5':
        hmacstr = hmac.HMAC(key.encode('utf8'), msg.encode('utf8'),
                            hashlib.md5).hexdigest()
        return hmacstr
    elif hashtype.lower() == 'sha224':
        hmacstr = hmac.HMAC(key.encode('utf8'), msg.encode('utf8'),
                            hashlib.sha224).hexdigest()
        return hmacstr
    elif hashtype.lower() == 'sha256':
        hmacstr = hmac.HMAC(key.encode('utf8'), msg.encode('utf8'),
                            hashlib.sha256).hexdigest()
        return hmacstr
    elif hashtype.lower() == 'sha512':
        hmacstr = hmac.HMAC(key.encode('utf8'), msg.encode('utf8'),
                            hashlib.sha512).hexdigest()
        return hmacstr
    else:
        raise NotImplementedError


def randomstr(leng=50):
    """
    Returns specified length random string including letters both upper and
    lower, and numbers.

    By default, the length is 50.
    """
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz'
                                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                 '0123456789'
                                 '')
                   for i in range(leng))


def is_python2():
    info = sys.version_info
    if info[0] == 2:
        return True
    else:
        return False


def is_python3():
    info = sys.version_info
    if info[0] == 3:
        return True
    else:
        return False


def load_shadowsocks_config(filename):
    """Returns shadowsocks config in a list."""
    assert os.path.isfile(filename)
    with open(filename) as f:
        j = json.load(f)
    for item in j:
        if is_python2():
            if isinstance(j[item], unicode):
                j[item] = j[item].encode("utf8")
    if "port_password" not in j:
        j["port_password"] = None
    if "workers" not in j:
        j["workers"] = 1
    if "user" not in j:
        j["user"] = None
    return j


def find_shadowsocks_config_file(deeply=False):
    """
    Find the shadowsocks config file in system.

    It will try in order as following:
        1. ./shadowsocks.json
        2. ~/shadowsocks.json
        3. ~/.shadowsocks.json
        4. /etc/shadowsocks.json
        5. /etc/shadowsocks/config.json
        6. /etc/shadowsocks-libev/config.json
    And returns the first one met (deeply == False, by default) or all the
    filenames that found (deeply == True).

    If there's nothing found, it returns None.
    """
    check_list = [
        os.path.abspath("shadowsocks.json"),
        os.path.join(os.environ["HOME"], "shadowsocks.json"),
        os.path.join(os.environ["HOME"], ".shadowsocks.json"),
        "/etc/shadowsocks.json",
        "/etc/shadowsocks/config.json",
        "/etc/shadowsocks-libev/config.json"]
    if not deeply:
        for filename in check_list:
            if os.path.isfile(filename):
                return filename
    else:
        config_files = []
        for filename in check_list:
            if os.path.isfile(filename):
                config_files += [filename]
        if config_files:
            return config_files
    return None


def info(msg):
    print(Fore.GREEN + msg + Fore.RESET)


def warn(msg):
    print(Fore.YELLOW + msg + Fore.RESET)


def err(msg):
    print(Fore.RED + msg + Fore.RESET)

# vim: tw=78 ts=8 et sw=4 sts=4 fdm=indent
