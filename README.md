# minecraft-mods-downloader

Control minecraft mods download easily with this tool.

## Install

Run:

```
pip install minecraft-mods-downloader
```

## Usage
Create a YAML file (`mod_list.yml` for example) that contains the list of mods you want using this format:

```yaml

A Nice Mod:
  version: 1.0
  mirrors:
    -
      url: http://somewhere/nice_mod-v1.0.zip
      extract_to: . #if should extract to minecraft folder
    -
      url: http://another_mirror/nice_mod-v1.0.jar #no need for extract_to here since it's only the jar file

Another Mod:
  version: A-1.0b
  mirrors:
    -
      url: http://somewhere/anothermod-vA-1.0b.zip
      extract_to: ./mods #if should extract to mods folder inside minecraft directory
    -
      url: http://another.place/anothermod-vA-1.0b.zip
      extract_to: . #some mirrors can use different zip files that need to be extracted to different places
    -
      url: http://another.place2/anothermod-vA-1.0b.jar
    -
      url: http://another.place3/anothermod-vA-1.0b.jar #you can have as many mirrors as you like, the first one that is working will be chosen to download the mod

```

Then run:

```
mine_mods -p <MINECRAFT_INSTALLATION_DIR> -f <MOD_LIST_YML_FILE>
```

Where <MINECRAFT_INSTALLATION_DIR> is the path to where you minecraft is installed, and <MOD_LIST_YML_FILE> is the path for the yaml file that lists the mods you want to download and install.

Ex:
```
mine_mods -p /home/my_user/.minecraft -f mod_list.yml
```

or you can pass a the url of a mod list file, ex:


```
mine_mods -p /home/my_user/.minecraft -f http://somewhere.com/mod_list.yml
```

Also, if you don't want to use cache, just add the `no-cached` flag when running the `mine_mods` command.


LICENSE
=============
This software is distributed using MIT license, see LICENSE file for more details.
