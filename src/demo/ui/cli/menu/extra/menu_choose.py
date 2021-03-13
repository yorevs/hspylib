#!/usr/bin/env python3
from hspylib.ui.cli.menu.extra.mchoose import mchoose

if __name__ == '__main__':
    it = [f"Item-{n}" for n in range(1, 21)]
    sel = mchoose(it)
    print(str(sel))
