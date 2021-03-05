#!/usr/bin/env python3
from hspylib.core.tools.text_helper import TextAlignment

from hspylib.ui.cli.tables.table_renderer import TableRenderer

if __name__ == '__main__':
    h = [
        'String',
        'Number',
        'Boolean',
        'That`s a big Integer Column Header'
    ]
    data = [
        ('One', 1, True, 2),
        ('Two', 2, False, 3),
        ('Three, four and five', 3, True, 3),
    ]
    tr = TableRenderer(h, data, 'TableRenderer example of usage')
    tr.adjust_sizes_by_largest_cell()
    tr.set_cell_alignment(TextAlignment.CENTER)
    tr.render()
