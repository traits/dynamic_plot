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
    if fname and "/" == fname[0]:
        return True
    return False


def format_resource(gen, metastring, formatter):
    """
    Create a list of URL-formatted script/style tags

    Parameters
    ----------
    gen: generator
        Pelican Generator
    metastring: string
        metadata['dp_scripts'] or metadata['dp_styles']
    formatter: string
        String format for output.

    Output
    ------
    List of formatted strings
    
    script = '<script type="module" src="{0}/js/{1}"></script>'
    metadata["dp_scripts"] = format_resource(gen, scripts, script)    
    """

    metalist = metastring.replace(" ", "").split(",")
    site_url = gen.settings["SITEURL"]
    return [formatter.format(site_url, x) for x in metalist]


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


csp = ""


def get_content_info(content):
    """
    Get path info for currently processed item here
    """

    scripts_location = content.metadata.get("dp_scripts_location")
    csp = content.relative_source_path  # content.metadata content.settings


def add_tags(gen, metadata):
    """
        The registered handler for the dynamic resources plugin. It will
        add the scripts and/or styles to the article
    """
    scripts = metadata.get("dynplot_scripts")
    if scripts:
        #  user scripts
        script = '<script type="module" src="{0}/js/{1}"></script>'
        metadata["dynplot_scripts"] = format_resource(gen, scripts, script)
        # D3 url
        url = get_effective_option(metadata, gen.settings, "dynplot_d3_url")
        url = f'<script src="{url}"></script>'
        metadata["dynplot_scripts"].insert(0, url)
        # three.js url
        url = get_effective_option(metadata, gen.settings, "dynplot_three_url")
        url = f'<script src="{url}"></script>'
        metadata["dynplot_scripts"].insert(0, url)
    styles = metadata.get("dynplot_styles")
    if styles:
        style = '<link rel="stylesheet" href="{0}/css/{1}" type="text/css" />'
        metadata["dynplot_styles"] = format_resource(gen, styles, style)
    csp = None


def copy_files_to_target(pelican):
    filemapping = {}
    pass


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
    signals.content_object_init.connect(get_content_info)
    signals.article_generator_context.connect(add_tags)
    signals.page_generator_context.connect(add_tags)
    signals.article_generator_finalized.connect(move_resources)
    signals.finalized.connect(copy_files_to_target)
