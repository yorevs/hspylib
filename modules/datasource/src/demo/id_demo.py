#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib-datasource
   @package: hspylib-datasource.demo
      @file: id_demo.py
   @created: Wed, 20 Mar 2024
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2024, HSPyLib team
"""

from collections import namedtuple
from datasource.identity import Identity
from hspylib.core.namespace import Namespace
from uuid import uuid4

if __name__ == "__main__":
    PersonId = namedtuple("PersonId", ["uuid"])
    UserId = namedtuple("UserId", ["uid", "email"])
    ns = Namespace(uuid=uuid4().hex)
    i1 = Identity.auto("uid")
    i2 = Identity(i1)
    i3 = Identity(UserId("12345", "user@example.com"))
    i4 = Identity(PersonId(uuid4().hex))
    i5 = Identity(ns)
    print("Identities: ", i1, i2, i3, i4, i5)
    print("Values: ", i1.values, i2.values, i3.values, i4.values, i5.values)
    print("Items: ", i1.items(), i2.items(), i3.items(), i4.items(), i5.items())
    print("Attrs/Values: ", i1.attributes, i1.values)
    print("Attrs/Values: ", i2.attributes, i2.values)
    print("Attrs/Values: ", i3.attributes, i3.values)
    print("Attrs/Values: ", i4.attributes, i4.values)
    print("Attrs/Values: ", i5.attributes, i5.values)
    print("As Dict: ", i1._asdict(), i2._asdict(), i3._asdict(), i4._asdict(), i5._asdict())
    print(
        "As ColSet: ",
        i1.as_column_set(),
        i2.as_column_set(),
        i3.as_column_set(),
        i4.as_column_set(),
        i5.as_column_set(),
    )
