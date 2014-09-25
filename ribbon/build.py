# -*- coding: utf-8 -*-

import yaml
import logging

log = None

def build(args):
    if args['debug']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    log = logging.getlogger(__name__)

    config = parse_config(path)
    log.debug('Config loaded: %s', config)

    dependencies(config)
    pre_build(config)
    source_build(config)
    post_build(config)
    init_scripts(config)
    pkg_scripts(config)
    build_package(config)
    publish_package(config)

def parse_config(path):
    log.debug('loading config from path: %s', path)
    try:
        with open(path) as f:
            return yaml.load(f)
    except EnvironmentError:
        log.error('Exception opening file at: %s', path)

def dependencies(config):
    raise NotImplementedError
def pre_build(config):
    raise NotImplementedError
def source_build(config):
    raise NotImplementedError
def post_build(config):
    raise NotImplementedError
def init_scripts(config):
    raise NotImplementedError
def  pkg_scripts(config):
    raise NotImplementedError
def  build_package(config):
    raise NotImplementedError
def  publish_package(config):
    raise NotImplementedError
