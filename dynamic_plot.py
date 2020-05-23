# -*- coding: utf-8 -*-
"""
Embedding D3 and three.js for Pelican
=====================================

This plugin allows you to easily embed D3 and three.js JS and CSS in Pelicans 
configuration and also the header of individual articles or pages. 
It also allows for for embedding article-specific D3.js versions.
"""

import os
import shutil
from pathlib import Path
import json
import logging

# import wingdbstub

from pelican import signals

logger = logging.getLogger(__name__)

DP_DEFAULT = {
    "dynplot_modules": True,
    "dynplot_d3_url": "https://d3js.org/d3.v5.min.js",
    "dynplot_three_url": "https://threejs.org/build/three.module.js",
}
DP_KEY = "DYNAMIC_PLOT_OPTIONS"
DP_MODULES_KEY = "dynplot_modules"
DP_SCRIPTS_KEY = "dynplot_scripts"
DP_STYLES_KEY = "dynplot_styles"

file_mapping = []


def init_default_config(pelican):
    """
    Write plugin defaults into pelican settings
    """

    from pelican.settings import DEFAULT_CONFIG

    def update_settings(settings):
        temp = DP_DEFAULT.copy()
        if DP_KEY in settings:
            temp.update(settings[DP_KEY])
        settings[DP_KEY] = temp
        return settings

    DEFAULT_CONFIG = update_settings(DEFAULT_CONFIG)
    if pelican:
        pelican.settings = update_settings(pelican.settings)


def get_effective_option(metadata, settings, key):
    """
    Return option with highest priority:
    not-defined key < default < pelican config settings < file metadata
    """

    return metadata.get(key, settings[DP_KEY].get(key))


def is_json(fname):
    """
    Returns True for string, enclosed with '[' ']', False else    
    """

    if str(fname) and (str(fname)[0] == "[") and (str(fname)[-1] == "]"):
        return True
    return False


def get_json(json_file):
    with open(json_file) as file:
        data = json.load(file)
    return list(data)


def is_relative(fname):
    """
    Returns True for leading '/', False else    
    """

    if str(fname) and (str(fname)[0] != "/"):
        return True
    return False


def copy_files_to_destination(gen):
    """
    Copy files to target destination
    """

    global file_mapping
    for m in file_mapping:
        if not m[0].exists():
            logger.warning(f"dynamic_plot: source file not found ({str(m[0])})")
            continue
        os.makedirs(os.path.dirname(str(m[1])), exist_ok=True)
        shutil.copy2(m[0], m[1])


def get_mapping(content, tag):
    """
    Return list of all file names from metadata enriched by
    input/output path information
    """

    # see format_tags
    if not hasattr(content, tag):
        return []

    files_str = getattr(content, tag)

    if not files_str:
        return []

    src_dir = Path(content.relative_dir)
    dst_dir = Path(content.url).parent
    content_root = Path(content.settings.get("PATH"))
    output_root = Path(content.settings.get("OUTPUT_PATH"))

    file_list = files_str.replace(" ", "").split(",")
    json_files = [e[1:-1] for e in file_list if is_json(e)]
    file_list = [e for e in file_list if not is_json(e)]

    for j in json_files:
        if is_relative(j):
            file_list += get_json(content_root / src_dir / j)
        else:
            file_list += get_json(content_root / j[1:])

    result = []
    for f in file_list:
        if is_relative(f):
            result.append([content_root / src_dir / f, output_root / dst_dir / f, f])
        else:
            result.append([content_root / f[1:], output_root / f[1:], f])

    return [[e[0].resolve(), e[1].resolve(), e[2]] for e in result]


def get_formatted_resource(content, tag, formatter):
    """
    Return list of html-tag-transformed raw filenames from metadata
    """

    # see format_tags
    if not hasattr(content, tag):
        return []

    files_str = getattr(content, tag)

    if not files_str:
        return []

    file_list = files_str.replace(" ", "").split(",")

    return [formatter.format(Path(f).as_posix()) for f in file_list]


def format_scripts(content, urls):
    def script_string(is_module, src):
        if is_module:
            return f'<script type="module" src="{src}"></script>'
        return f'<script src="{src}"></script>'

    use_modules = get_effective_option(
        content.metadata, content.settings, DP_SCRIPTS_KEY
    )

    entries = [script_string(use_modules, Path(f).as_posix()) for f in urls]

    if entries:
        #  user scripts
        ## Take care here, NOT to try modifying content.metadata["dynplot_scripts"]
        ## These will no longer affect the values used for html output after
        ## content creation
        content.dynplot_scripts = [x for x in entries]
        #  master scripts
        for url_tag in ["dynplot_d3_url", "dynplot_three_url"]:
            url = get_effective_option(content.metadata, content.settings, url_tag)
            url = script_string(use_modules, url)
            content.dynplot_scripts.insert(0, url)


def format_styles(content, urls):
    entries = [
        f'<link rel="stylesheet" href="{Path(f).as_posix()}" type="text/css" />'
        for f in urls
    ]
    if entries:
        #  user scripts
        ## Take care here, NOT to try modifying content.metadata["dynplot_styles"]
        ## These will no longer affect the values used for html output after
        ## content creation
        content.dynplot_styles = [x for x in entries]


def add_files(content):
    """
    Receive content and extract relevant information for later usage
    """

    scripts = get_mapping(content, DP_SCRIPTS_KEY)
    styles = get_mapping(content, DP_STYLES_KEY)
    global file_mapping
    if scripts:
        file_mapping += [[s[0], s[1]] for s in scripts]
        format_scripts(content, [s[2] for s in scripts])
    if styles:
        file_mapping += [[s[0], s[1]] for s in styles]
        format_styles(content, [s[2] for s in styles])


def register():
    """
    Plugin registration
    """

    signals.initialized.connect(init_default_config)
    signals.content_object_init.connect(add_files)
    signals.finalized.connect(copy_files_to_destination)
