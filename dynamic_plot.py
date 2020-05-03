# -*- coding: utf-8 -*-
"""
Embedding D3 and three.js for Pelican
=====================================

This plugin allows you to easily embed D3 and three.js JS and CSS in Pelicans configuration and also the header of individual articles. It also allows for single-tag embedding of D3.js.
"""
import os
import shutil
from pathlib import Path

# import wingdbstub

from pelican import signals

DP_DEFAULT = {
    "dynplot_d3_url": "https://d3js.org/d3.v5.min.js",
    "dynplot_three_url": "https://threejs.org/build/three.min.js",
}
DP_KEY = "DYNAMIC_PLOT_OPTIONS"
DP_SCRIPTS_KEY = "dynplot_scripts"
DP_STYLES_KEY = "dynplot_styles"

# hack: (see https://github.com/getpelican/pelican-plugins/issues/1260)
# We need the following temporary keys to maintain the original metadata
# before they are converted into html tags in format_tags in order
# to be able to use them in add_files.
# Somewhere between the calls of the signals for article_generator_context (format_tags)
# and article_generator_write_article (add_files) the metadata with the original key
# is written using the themes template, so the html tag conversion cannot be postponed to
# the article_generator_write_article handler.

DP_SCRIPTS_KEY_TMP = DP_SCRIPTS_KEY + "_"
DP_STYLES_KEY_TMP = DP_STYLES_KEY + "_"

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


def copy_resources(gen):
    global file_mapping
    for m in file_mapping:
        os.makedirs(os.path.dirname(str(m[1])), exist_ok=True)
        shutil.copy2(m[0], m[1])


def get_mapping(gen, content, tag):
    metadata = content.metadata
    src_dir = Path(content.relative_dir)
    dst_dir = Path(content.url).parent
    content_root = Path(gen.path)
    output_root = Path(gen.output_path)

    files_str = metadata.get(tag)

    if not files_str:
        return []

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


def get_formatted_resource(metadata, tag, formatter):
    files_str = metadata.get(tag)

    if not files_str:
        return []

    file_list = files_str.replace(" ", "").split(",")

    return [formatter.format(Path(f).as_posix()) for f in file_list]


def format_tags(gen, metadata):
    scripts = get_formatted_resource(
        metadata, DP_SCRIPTS_KEY, '<script type="module" src="{0}"></script>'
    )
    styles = get_formatted_resource(
        metadata, DP_STYLES_KEY, '<link rel="stylesheet" href="{0}" type="text/css" />',
    )
    if scripts:
        #  user scripts
        metadata[DP_SCRIPTS_KEY_TMP] = metadata[DP_SCRIPTS_KEY]
        metadata[DP_SCRIPTS_KEY] = [x for x in scripts]
        #  master scripts
        for url_tag in ["dynplot_d3_url", "dynplot_three_url"]:
            url = get_effective_option(metadata, gen.settings, url_tag)
            url = f'<script src="{url}"></script>'
            metadata[DP_SCRIPTS_KEY].insert(0, url)
    if styles:
        # user styles
        metadata[DP_STYLES_KEY_TMP] = metadata[DP_STYLES_KEY]
        metadata[DP_STYLES_KEY] = [x for x in styles]


def add_files(gen, content):
    """
    Receive generator and content and extract relevant information
    """

    scripts = get_mapping(gen, content, DP_SCRIPTS_KEY_TMP)
    styles = get_mapping(gen, content, DP_STYLES_KEY_TMP)
    global file_mapping
    if scripts:
        file_mapping += scripts
    if styles:
        file_mapping += styles


def register():
    """
        Plugin registration
    """
    signals.initialized.connect(init_default_config)
    signals.article_generator_context.connect(format_tags)
    signals.page_generator_context.connect(format_tags)
    signals.article_generator_write_article.connect(add_files)
    signals.page_generator_write_page.connect(add_files)
    signals.finalized.connect(copy_resources)
