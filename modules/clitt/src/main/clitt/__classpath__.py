#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt
      @file: __classpath__.py
   @created: Fri, 23 Dec 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from hspylib.core.metaclass.classpath import Classpath
from hspylib.core.tools.commons import parent_path, root_dir


class _Classpath(Classpath):
    """Provide a class to help locating user-defined classes, packages, sources and resources."""

    def __init__(self):
        super().__init__(parent_path(__file__), parent_path(root_dir()), (parent_path(__file__) / "resources"))


# Instantiate the classpath singleton
assert (classpath := _Classpath()) is not None, "Failed to create Classpath instance"
