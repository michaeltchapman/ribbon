# -*- coding: utf-8 -*-

import yaml
import logging

log = False
noop = False

def build(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    global log
    log = logging.getLogger('build')
    noop = args.noop
    config = parse_config(args.path[0])
    log.debug('Config loaded: %s', config)

    return

    upstreams(config)
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

def upstreams(config):
    raise NotImplementedError
def pre_build(config):
    raise NotImplementedError
def source_build(config):
    raise NotImplementedError
def post_build(config):
    raise NotImplementedError
def init_scripts(config):
    raise NotImplementedError
def pkg_scripts(config):
    raise NotImplementedError
def build_package(config):
    raise NotImplementedError
def publish_package(config):
    raise NotImplementedError
