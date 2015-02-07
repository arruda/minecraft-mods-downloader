#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib, urllib2
import urlparse

import yaml

MINECRAFT_PATH = os.environ.get("MINECRAFT_PATH", "/home/arruda/projetos/minecraft-mods-downloader/mc")
CACHED_PATH = os.path.join(MINECRAFT_PATH, 'cache')


def read_mod_list():
    stream = open("mod_list.yml", 'r')
    mod_list = yaml.load(stream)
    return mod_list


def get_filename(url):
    path = urlparse.urlsplit(url).path
    filename = path.split('/')[-1]
    return filename


def get_mod_url(name, data):
    for url in data.get('url'):

        try:
            urllib2.urlopen(url)
            return url
        except Exception, e:
            print(e)

    raise Exception("No url for %s" % name)


def download_mod(name, url):
    filename = get_filename(url)
    file_path = os.path.join(CACHED_PATH, filename)

    print "saving to: %s" % file_path
    file_downloader = urllib.URLopener()
    file_downloader.retrieve(url, file_path)
    return file_path


def install_mods(client=True):
    mod_list = read_mod_list()

    for mod, data in mod_list.items():
        working_url = get_mod_url(mod, data)
        print "Downloading %(mod)s from %(url)s" % {'mod': mod, 'url': working_url}
        zip_filepath = download_mod(mod, working_url)

    print "Done!"


if __name__ == '__main__':
    # MINECRAFT_PATH = "/home/arruda/projetos/minecraft-mods-downloader/mc"

    if not os.path.exists(CACHED_PATH):
        os.makedirs(CACHED_PATH)
    install_mods()
    # func_name = sys.argv[1]
    # task = globals()[func_name]

    # try:
    #     task(sys.argv[2:])
    # except:
