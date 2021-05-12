#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.versioner.src.main
      @file: __main__.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from versioner.src.main.core.versioner import Versioner

if __name__ == '__main__':
    files = sys.argv[1:]
    v = Versioner('0.10.4', '/Users/hugo/GIT-Repository/GitHub/Python/hspylib', files)
    v.patch()
    v.save()
    print(v.version)
