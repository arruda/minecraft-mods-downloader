#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml


def read_mod_list():
    stream = open("mod_list.yml", 'r')
    mod_list = yaml.load(stream)
    return mod_list

def install_mods(client=True):
    mod_list = read_mod_list()

    for mod, data in mod_list.items():



if __name__ == '__main__':

    read_mod_list()
    # func_name = sys.argv[1]
    # task = globals()[func_name]

    # try:
    #     task(sys.argv[2:])
    # except: