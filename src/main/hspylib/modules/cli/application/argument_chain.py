#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.application
      @file: argument_chain.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any

from hspylib.modules.cli.application.argument import Argument


class ArgumentChain:
    @staticmethod
    class ArgumentChainBuilder:
        
        def __init__(self):
            self.chained_arguments = set()
        
        def when(self, arg_name: str, val_regex: str, required: bool = True) -> Any:
            argument = Argument(arg_name, val_regex, required)
            next_in_chain = ArgumentChain.ChainedArgument(self, argument)
            self.chained_arguments.add(next_in_chain)
            return next_in_chain

        def just(self, arg_name: str, val_regex: str, required: bool = True) -> Any:
            argument = Argument(arg_name, val_regex, required)
            self.chained_arguments.add(ArgumentChain.ChainedArgument(self, argument))
            return self
        
        def build(self) -> set:
            return self.chained_arguments
    
    @staticmethod
    class ChainedArgument:
        
        def __init__(self, parent, argument: Argument):
            self.parent = parent
            self.argument = argument
        
        def __str__(self):
            return str(self.argument)
        
        def accept(self, arg_name: str, val_regex) -> Any:
            argument = Argument(arg_name, val_regex, False)
            next_in_chain = ArgumentChain.ChainedArgument(self.parent, argument)
            self.argument.set_next(argument)
            return next_in_chain
        
        def require(self, arg_name: str, val_regex) -> Any:
            argument = Argument(arg_name, val_regex)
            next_in_chain = ArgumentChain.ChainedArgument(self.parent, argument)
            self.argument.set_next(argument)
            return next_in_chain
        
        def end(self) -> Any:
            return self.parent
    
    @classmethod
    def builder(cls) -> Any:
        return cls.ArgumentChainBuilder()
