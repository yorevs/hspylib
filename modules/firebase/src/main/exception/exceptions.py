#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.exception
      @file: exceptions.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.core.exception.exceptions import HSBaseException

class FirebaseAuthenticationError(HSBaseException):
    """Raised when authenticate to Firebase"""

class InvalidFirebaseCredentials(HSBaseException):
    """Raised when invalid credentials are provided to Firebase"""

class FirebaseException(HSBaseException):
    """Raised when Firebase module raises an error"""
