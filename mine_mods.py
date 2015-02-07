#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ntpath
import os
import shutil
import urllib
import urllib2
import urlparse
import zipfile

import yaml


MINECRAFT_PATH = os.environ.get("MINECRAFT_PATH", "/home/arruda/projetos/minecraft-mods-downloader/mc")
CACHED_PATH = os.path.join(MINECRAFT_PATH, 'cache')
MODS_PATH = os.path.join(MINECRAFT_PATH, 'mods')


def read_mod_list():
    stream = open("mod_list.yml", 'r')
    mod_list = yaml.load(stream)
    return mod_list


def get_filename(url):
    path = urlparse.urlsplit(url).path
    filename = path.split('/')[-1]
    return filename


def get_mod_working_mirror(name, data):
    for mirror in data.get('mirrors'):
        url = mirror.get('url')
        try:
            urllib2.urlopen(url)
            return mirror
        except Exception, e:
            print(e)

    raise Exception("No url for %s" % name)


def is_mod_cached(cached_filepath):
    return os.path.exists(cached_filepath)


def download_mod(name, url):
    filename = get_filename(url)
    file_path = os.path.join(CACHED_PATH, filename)
    if is_mod_cached(file_path):
        print "Using cache %s" % file_path
    else:
        print "Saving to: %s" % file_path
        file_downloader = urllib.URLopener()
        file_downloader.retrieve(url, file_path)
    return file_path


def unzip_mod_to_mods_path(name, filepath, extract_to):
    file_unzip_path = os.path.join(MINECRAFT_PATH, extract_to)
    print "Extracting %(mod)s to %(path)s" % {'mod': name, 'path': file_unzip_path}

    with zipfile.ZipFile(filepath, "r") as z:
        z.extractall(file_unzip_path)

    return file_unzip_path


def copy_mod_to_mods_path(name, filepath):
    print "Copying %(mod)s to %(path)s" % {'mod': name, 'path': MODS_PATH}
    filename = ntpath.basename(filepath)
    dest_path = os.path.join(MODS_PATH, filename)
    shutil.copyfile(filepath, dest_path)
    return dest_path


def install_mods(client=True):
    mod_list = read_mod_list()

    for mod, data in mod_list.items():
        working_mirror = get_mod_working_mirror(mod, data)
        download_url = working_mirror.get('url')
        print "Downloading %(mod)s from %(url)s" % {'mod': mod, 'url': download_url}
        filepath = download_mod(mod, download_url)

        if working_mirror.get('extract_to', None):
            unzip_mod_to_mods_path(mod, filepath, working_mirror.get('extract_to'))
        else:
            copy_mod_to_mods_path(mod, filepath)
            pass

        print "Installed %(mod)s version:%(version)s" % {'mod': mod, 'version': data.get('version')}

    print "Done!"


if __name__ == '__main__':

    if not os.path.exists(CACHED_PATH):
        os.makedirs(CACHED_PATH)

    if not os.path.exists(MODS_PATH):
        os.makedirs(MODS_PATH)

    install_mods()
    # func_name = sys.argv[1]
    # task = globals()[func_name]

    # try:
    #     task(sys.argv[2:])
    # except:
