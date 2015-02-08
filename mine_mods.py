#!/usr/bin/env python
# -*- coding: utf-8 -*-
from contextlib import closing
import ntpath
import os
import shutil
import urllib
import urllib2
import urlparse
import zipfile

import click
import yaml

MINECRAFT_PATH = "."
CACHED_PATH = os.path.join(MINECRAFT_PATH, 'cache')
MODS_PATH = os.path.join(MINECRAFT_PATH, 'mods')


def read_mod_list(mod_list_path):
    if 'http' in mod_list_path:
        with closing(urllib2.urlopen(mod_list_path)) as f:
            mod_list = yaml.load(f)
    else:
        with open(mod_list_path, 'r') as f:
            mod_list = yaml.load(f)
    return mod_list


def get_filename(url):
    path = urlparse.urlsplit(url).path
    filename = path.split('/')[-1]
    return filename


def get_mod_working_mirror(name, data):
    for mirror in data.get('mirrors'):
        url = mirror.get('url')
        try:
            urllib2.urlopen(url, timeout=5)
            return mirror
        except Exception, e:
            click.echo(
                "<Warning>: Mirror with url (%(url)s) not working: %(msg)s" %
                {'url': url, 'msg': e}
            )

    raise Exception("No working url for %s mod" % name)


def is_mod_cached(cached_filepath):
    return os.path.exists(cached_filepath)


def download_mod(name, url, no_cache):
    filename = get_filename(url)
    file_path = os.path.join(CACHED_PATH, filename)
    if is_mod_cached(file_path) and not no_cache:
        click.echo("Using cache %s" % file_path)
    else:
        click.echo("Downloading to: %s" % file_path)
        file_downloader = urllib.URLopener()
        file_downloader.retrieve(url, file_path)
    return file_path


def unzip_mod_to_mods_path(name, filepath, extract_to):
    file_unzip_path = os.path.join(MINECRAFT_PATH, extract_to)
    click.echo("Extracting %(mod)s to %(path)s" % {'mod': name, 'path': file_unzip_path})

    with zipfile.ZipFile(filepath, "r") as z:
        z.extractall(file_unzip_path)

    return file_unzip_path


def copy_mod_to_mods_path(name, filepath):
    click.echo("Copying %(mod)s to %(path)s" % {'mod': name, 'path': MODS_PATH})
    filename = ntpath.basename(filepath)
    dest_path = os.path.join(MODS_PATH, filename)
    shutil.copyfile(filepath, dest_path)
    return dest_path


def set_global_paths(minecraft_path):
    global MINECRAFT_PATH, CACHED_PATH, MODS_PATH
    MINECRAFT_PATH = minecraft_path
    CACHED_PATH = os.path.join(MINECRAFT_PATH, 'cache')
    MODS_PATH = os.path.join(MINECRAFT_PATH, 'mods')


def ensure_paths_exist():
    if not os.path.exists(CACHED_PATH):
        os.makedirs(CACHED_PATH)

    if not os.path.exists(MODS_PATH):
        os.makedirs(MODS_PATH)


@click.command()
@click.option('-p',
              'minecraft_path',
              default='.',
              type=click.Path(exists=True, dir_okay=True, resolve_path=True),
              help='Path to minecraft instalation directory')
@click.option('-f',
              '--url',
              'mod_list_path',
              default='.',
              # type=click.Path(exists=True, file_okay=True, resolve_path=True),
              help='Path (or url) to mod list yaml file')
@click.option('--no-cache', is_flag=True,
              help='Do not use cache when installing mods')
def install_mods(minecraft_path, mod_list_path, no_cache):
    set_global_paths(minecraft_path)
    ensure_paths_exist()
    mod_list = read_mod_list(mod_list_path)

    for mod, data in mod_list.items():
        working_mirror = get_mod_working_mirror(mod, data)
        download_url = working_mirror.get('url')
        click.echo("Fetching %(mod)s from %(url)s" % {'mod': mod, 'url': download_url})
        filepath = download_mod(mod, download_url, no_cache)

        if working_mirror.get('extract_to', None):
            unzip_mod_to_mods_path(mod, filepath, working_mirror.get('extract_to'))
        else:
            copy_mod_to_mods_path(mod, filepath)

        click.echo("Installed %(mod)s version:%(version)s" % {'mod': mod, 'version': data.get('version')})

    click.echo("Done!")

if __name__ == '__main__':
    install_mods()
