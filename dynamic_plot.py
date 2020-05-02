# -*- coding: utf-8 -*-
"""
Embedding D3 and three.js for Pelican
=====================================

This plugin allows you to easily embed D3 and three.js JS and CSS in Pelicans configuration and also the header of individual articles. It also allows for single-tag embedding of D3.js.
"""
import os
import shutil
from pathlib import Path

import wingdbstub

from pelican import signals

DP_DEFAULT = {
    "dynplot_d3_url": "https://d3js.org/d3.v5.min.js",
    "dynplot_three_url": "https://threejs.org/build/three.min.js",
}
DP_KEY = "DYNAMIC_PLOT_OPTIONS"

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


def copy_resources(src, dest, file_list):
    """
    Copy files from content folder to output folder

    Parameters
    ----------
    src: string
        Content folder path
    dest: string,
        Output folder path
    file_list: list
        List of files to be transferred

    Output
    ------
    Copies files from content to output
    """
    if not os.path.exists(dest):
        os.makedirs(dest)
    for file_ in file_list:
        file_src = os.path.join(src, file_)
        shutil.copy2(file_src, dest)


def get_mapping(gen, content, tag, formatter):
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

        url = Path(f).as_posix()
        include = formatter.format(url)
        result.append([src.resolve(), dst.resolve(), include])

    return result


def evaluate_tags(gen, content):
    """
    Receive generator, content and metadata at a single point
    and extract relevant information
    """
    metadata = content.metadata
    scripts = get_mapping(
        gen, content, "dynplot_scripts", '<script type="module" src="{0}"></script>',
    )
    styles = get_mapping(
        gen,
        content,
        "dynplot_styles",
        '<link rel="stylesheet" href="{0}" type="text/css" />',
    )
    global file_mapping
    if scripts:
        file_mapping += scripts
        #  user scripts
        metadata["dynplot_scripts"] = [x[2] for x in scripts]
        #  master scripts
        for url_tag in ["dynplot_d3_url", "dynplot_three_url"]:
            url = get_effective_option(metadata, gen.settings, url_tag)
            url = f'<script src="{url}"></script>'
            metadata["dynplot_scripts"].insert(0, url)
    if styles:
        file_mapping += styles
        # user styles
        metadata["dynplot_styles"] = [x[2] for x in styles]


def move_resources(gen):
    """
    Move files from js/css folders to output folder
    """
    js_files = gen.get_files("js", extensions="js")
    css_files = gen.get_files("css", extensions="css")

    js_dest = os.path.join(gen.output_path, "js")
    copy_resources(gen.path, js_dest, js_files)

    css_dest = os.path.join(gen.output_path, "css")
    copy_resources(gen.path, css_dest, css_files)


def register():
    """
        Plugin registration
    """
    signals.initialized.connect(init_default_config)
    signals.article_generator_write_article.connect(evaluate_tags)
    signals.page_generator_write_page.connect(evaluate_tags)
    signals.article_generator_finalized.connect(move_resources)
    # signals.finalized.connect(copy_files_to_target)
