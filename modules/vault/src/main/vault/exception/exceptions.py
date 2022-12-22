#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Vault
   @package: vault.exception
      @file: exceptions.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.core.exception.exceptions import HSBaseException


class VaultCloseError(HSBaseException):
    """Raised when closing the vault"""


class VaultOpenError(HSBaseException):
    """Raised when opening the vault"""


class VaultSecurityException(HSBaseException):
    """Raised when something unexpected happened to vault file"""


class VaultExecutionException(HSBaseException):
    """Raised when something unexpected happened to vault execution"""
