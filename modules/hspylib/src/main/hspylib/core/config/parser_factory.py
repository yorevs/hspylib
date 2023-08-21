#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.config
      @file: parser_factory.py
   @created: Wed, 19 May 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import os
import re
from abc import ABC
from configparser import ConfigParser
from functools import partial
from typing import Any, Callable, Dict, TextIO, TypeAlias

import toml
import yaml

from hspylib.core.tools.dict_tools import flatten_dict

Properties : TypeAlias = Dict[str, Any]


class ParserFactory(ABC):
    """Provide a properties parser factory."""

    class PropertyParser:
        """Represent a property parser."""

        def __init__(self, parser: Callable[[TextIO], Properties]):
            self._parser = parser

        def parse(self, file_handler: TextIO) -> Properties:
            return self._parser(file_handler)

    @staticmethod
    def _read_properties(file_handler: TextIO) -> Properties:
        """Reads properties from properties file (key and element pairs) from the input list."""
        all_lines = list(map(str.strip, filter(None, file_handler.readlines())))
        # fmt: off
        return {
            p[0].strip(): p[1].strip()
            for p in [
                p.split("=", 1) for p in list(
                    filter(lambda l: re.match(r"[a-zA-Z]([.\\-]|\w)* *= *.+", l), all_lines)
                )
            ]
        }
        # fmt: off

    @staticmethod
    def _read_cfg_or_ini(file_handler: TextIO) -> Properties:
        """Reads properties from a cfg or ini file (key and element pairs) from the input list."""
        all_lines = list(map(str.strip, filter(None, file_handler.readlines())))
        string = os.linesep.join(all_lines)
        all_cfgs = {}
        cfg = ConfigParser()
        cfg.read_string(string)
        for section in cfg.sections():
            all_cfgs.update(dict(cfg.items(section)))
        return all_cfgs

    @staticmethod
    def _read_yaml(file_handler: TextIO) -> Properties:
        """Reads properties from a yaml file (key and element pairs) from the input list."""
        return flatten_dict(yaml.safe_load(file_handler))

    @staticmethod
    def _read_toml(file_handler: TextIO) -> Properties:
        """Reads properties from a toml file (key and element pairs) from the input list."""
        return flatten_dict(toml.load(file_handler))

    @classmethod
    def create(cls, file_extension: str) -> PropertyParser:
        if file_extension in [".ini", ".cfg"]:
            parser = partial(cls._read_cfg_or_ini)
        elif file_extension == ".properties":
            parser = partial(cls._read_properties)
        elif file_extension in [".yml", ".yaml"]:
            parser = partial(cls._read_yaml)
        elif file_extension == ".toml":
            parser = partial(cls._read_toml)
        else:
            raise NotImplementedError(f"Extension {file_extension} is not supported")

        return cls.PropertyParser(parser)
