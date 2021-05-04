#!/usr/bin/env python3
from hspylib.modules.cli.menu.extra.mselect import mselect

if __name__ == '__main__':
    it = [f"Item-{n}" for n in range(1, 21)]
    sel = mselect(it)
    print(str(sel))
