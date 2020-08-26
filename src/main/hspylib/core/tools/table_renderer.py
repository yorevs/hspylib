import sys
from typing import List, Optional, Callable

from main.hspylib.core.tools.text_helper import TextJustify

MIN_COL_LENGTH = 6


class CellJustify(Callable):
    """
    Table cell text justification helper.
    """
    LEFT = TextJustify.justify_left
    CENTER = TextJustify.justify_center
    RIGHT = TextJustify.justify_right


class TableRenderer:

    def __init__(self, headers: List[str], table_data: Optional[iter], caption: str = None):
        """
        :param headers: table headers to be displayed.
        :param table_data: table record set with the selected rows.
        :param caption: table caption to be displayed.
        """
        self.headers = headers
        self.data = table_data
        self.caption = caption
        self.head_justify = CellJustify.CENTER
        self.cell_justify = CellJustify.LEFT
        self.rows = [r for r in self.data] if self.data else []

    def set_header_justify(self, justify: CellJustify = CellJustify.CENTER) -> None:
        """
        Set table header justification.
        :param justify: table header text justification function.
        :return:
        """
        self.head_justify = justify

    def set_cell_justify(self, justify: CellJustify = CellJustify.LEFT) -> None:
        """
        Set table header justification.
        :param justify: table cell text justification function.
        :return:
        """
        self.cell_justify = justify

    def render(
            self,
            file=sys.stdout) -> None:
        """
        Render table based on the maximum length between a column data and header. Data will not be wrapped.
        :param file: a file-like object (stream); defaults to the current sys.stdout.
        :return: None
        """
        if self.rows:
            assert len(min(self.rows, key=len)) == len(self.headers), \
                f'Headers and Columns must have the same size: {len(min(self.rows, key=len))} vs {len(self.headers)}'
        column_sizes = [max(MIN_COL_LENGTH, len(header)) for header in self.headers]
        for row in self.rows:
            for idx in range(0, len(row)):
                column_sizes[idx] = max(column_sizes[idx], len(str(row[idx])))
        indexes = range(0, len(column_sizes))
        header_cols = [
            '| ' + ' | '.join(self.head_justify(self.headers[idx], column_sizes[idx]) for idx in indexes) + ' |']
        table_line = '+' + ''.join((('-' * (column_sizes[idx] + 2) + '+') for idx in indexes))
        data_cols = [
            '| ' +
            ''.join('%s | ' % self.cell_justify(str(row[idx]), column_sizes[idx]) for idx in indexes) for row in
            self.rows
        ]
        self.__print_table(table_line, header_cols, data_cols, file)

    def __print_table(
            self,
            table_line: str,
            header_cols: List[str],
            data_cols: List[str],
            file=sys.stdout) -> None:
        """
        Print the table to stdout or to a file.
        :param table_line: table border lines
        :param header_cols: table headers to be displayed.
        :param data_cols: table data to be displayed.
        :param file: a file-like object (stream); defaults to the current sys.stdout.
        :return: None
        """
        if self.caption:
            print(table_line, file=file)
            print('| ' + self.caption[0:len(table_line) - 4].center(len(header_cols[0]) - 4, ' ') + ' |', file=file)
        print(table_line, file=file)
        print('\n'.join(header_cols), file=file)
        print(table_line, file=file)
        print(
            '\n'.join(data_cols) if data_cols
            else '| ' + '<empty>'.center(len(table_line) - 4, ' ') + ' |', file=file
        )
        print(table_line, file=file)


if __name__ == '__main__':
    h = [
        'Col 1',
        'Columns 2',
        'Columns 3',
        'Thats a big Column Header'
    ]
    data = [
        ('One', 1, True, 2),
        ('Two', 2, False, 3),
        ('Three, four and five', 3, True, 3),
    ]
    tr = TableRenderer(h, data, 'TableRenderer example of usage')
    tr.render()
