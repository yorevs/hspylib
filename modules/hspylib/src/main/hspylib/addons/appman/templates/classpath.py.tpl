#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hspylib.core.metaclass.classpath import Classpath
from hspylib.core.tools.commons import get_path, run_dir


class _Classpath(Classpath):
  """TODO"""

  def __init__(self):
    super().__init__(
      get_path(__file__),
      get_path(run_dir()),
      (get_path(__file__) / "resources"))


# Instantiate the classpath singleton
_Classpath()
