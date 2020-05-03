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
import logging

# import wingdbstub

from pelican import signals

logger = logging.getLogger(__name__)

DP_DEFAULT = {
    "dynplot_d3_url": "https://d3js.org/d3.v5.min.js",
    "dynplot_three_url": "https://threejs.org/build/three.min.js",
}
DP_KEY = "DYNAMIC_PLOT_OPTIONS"
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


def is_relative(fname):
    """
    Returns True for leading '/', False else    
    """

    if fname and (fname[0] != "/"):
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

    result = []
    for f in file_list:
        src = None
        dst = None
        if is_relative(f):
            src = content_root / src_dir / f
            dst = output_root / dst_dir / f
        else:
            src = content_root / f[1:]
            dst = output_root / f[1:]

        result.append([src.resolve(), dst.resolve()])

    return result


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


def format_tags(content):
    """
    Provide html <script> and <link> tags for script/css files from metadata 
    """

    scripts = get_formatted_resource(
        content, DP_SCRIPTS_KEY, '<script type="module" src="{0}"></script>'
    )
    styles = get_formatted_resource(
        content, DP_STYLES_KEY, '<link rel="stylesheet" href="{0}" type="text/css" />',
    )
    if scripts:
        #  user scripts
        ## Take care here, NOT to try modifying content.metadata["dynplot_scripts"]
        ## etc.. These will no longer affect the values used for html output after
        ## content creation
        content.dynplot_scripts = [x for x in scripts]
        #  master scripts
        for url_tag in ["dynplot_d3_url", "dynplot_three_url"]:
            url = get_effective_option(content.metadata, content.settings, url_tag)
            url = f'<script src="{url}"></script>'
            content.dynplot_scripts.insert(0, url)
    if styles:
        # user styles
        content.dynplot_styles = [x for x in styles]


def add_files(content):
    """
    Receive content and extract relevant information for later usage
    """

    scripts = get_mapping(content, DP_SCRIPTS_KEY)
    styles = get_mapping(content, DP_STYLES_KEY)
    global file_mapping
    if scripts:
        file_mapping += scripts
    if styles:
        file_mapping += styles

    format_tags(content)


def register():
    """
    Plugin registration
    """

    signals.initialized.connect(init_default_config)
    signals.content_object_init.connect(add_files)
    signals.finalized.connect(copy_files_to_destination)
